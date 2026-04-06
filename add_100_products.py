import os
import django
import random
import requests
from django.core.files.base import ContentFile
import concurrent.futures

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hardware_store.settings')
django.setup()

from chatbot.models import Product

def download_image(seed):
    # loremflickr provides distinct random images based on the lock parameter
    # using 'hardware,tool' as keywords to get relevant images
    url = f"https://loremflickr.com/400/400/hardware,tool,equipment?lock={seed}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.content
    except Exception as e:
        print(f"Error downloading image {seed}: {e}")
    return None

def main():
    adjectives = [
        "Professional", "Heavy-Duty", "Precision", "Industrial", 
        "Cordless", "Magnetic", "High-Torque", "Compact", 
        "Ergonomic", "Titanium", "Carbon Steel", "Brushless", 
        "Lithium-Ion", "Waterproof", "Shockproof", "Heavy", "Lightweight"
    ]
    tools = [
        "Hammer", "Impact Drill", "Screwdriver Set", "Wrench", 
        "Pliers", "Tape Measure", "Laser Level", "Circular Saw", 
        "Angle Grinder", "Belt Sander", "Digital Multimeter", 
        "LED Work Light", "Rolling Toolbox", "Safety Goggles", 
        "Bench Vise", "Air Compressor", "Nail Gun", "Rotary Tool"
    ]
    
    # Pre-download a pool of 20 distinct images to avoid 100 slow network requests
    print("Fetching 20 sample images related to hardware tools...")
    image_pool = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(download_image, i): i for i in range(1, 21)}
        for future in concurrent.futures.as_completed(futures):
            img_content = future.result()
            if img_content:
                image_pool.append(img_content)
                
    if not image_pool:
        print("Failed to download any images. Please check your internet connection.")
        return
        
    print(f"Successfully downloaded {len(image_pool)} sample images.")
    print("Generating 100 unique products...")
    
    products_created = 0
    
    for i in range(1, 101):
        name = f"{random.choice(adjectives)} {random.choice(tools)} Gen-{i}"
        description = f"Engineered for the toughest jobs, this {name.lower()} offers unmatched durability and precision. Perfect for both DIY enthusiasts and professional contractors."
        price = round(random.uniform(999, 35000), 2)
        stock_quantity = random.randint(0, 150)
        discount = random.choice([0.00, 0.00, 0.00, 500.00, 1000.00, 1500.00])
        
        p, created = Product.objects.update_or_create(
            name=name,
            defaults={
                'description': description,
                'price': price,
                'stock_quantity': stock_quantity,
                'discount': discount
            }
        )
        
        # Pick a random image from the pre-downloaded pool to prevent 100 slow HTTP requests
        img_content = random.choice(image_pool)
        file_name = f"sample_product_{i}.jpg"
        
        p.image.save(file_name, ContentFile(img_content), save=True)
        products_created += 1
        
        if i % 10 == 0:
            print(f"[{i}/100] Processed {p.name}...")
            
    print(f"Done! Successfully added {products_created} products with sample images.")

if __name__ == "__main__":
    main()
