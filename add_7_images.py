import os
import django
import requests
from django.core.files.base import ContentFile
import urllib.parse

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hardware_store.settings')
django.setup()

from chatbot.models import Product

def main():
    products_to_update = {
        "Titanium Claw Hammer": "hammer,tool",
        "Brushless Impact Drill": "drill,power tool",
        "Magnetic Tape Measure": "measuring tape,tool",
        "Workbench Vise": "vise,workshop",
        "Precision Laser Level 360°": "laser level,equipment",
        "Pro Safety Gear Set": "safety glasses,construction",
        "Engineer's Scale Ruler": "ruler,engineering"
    }
    
    for name, keywords in products_to_update.items():
        try:
            product = Product.objects.get(name__iexact=name)
            
            # Using LoremFlickr to get relevant random images based on search keywords
            url = f"https://loremflickr.com/400/400/{urllib.parse.quote(keywords)}/all"
            
            print(f"Downloading image for '{name}' using keywords '{keywords}'...")
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                # Clean up filename
                safe_name = name.replace(' ', '_').replace('°', '').replace("'", "")
                file_name = f"{safe_name}.jpg"
                
                # Save the image content directly to the ImageField
                product.image.save(file_name, ContentFile(response.content), save=True)
                print(f"✅ Successfully added image to {name}.")
            else:
                print(f"❌ Failed to download image for {name}. HTTP Status: {response.status_code}")
                
        except Product.DoesNotExist:
            print(f"⚠️ Product '{name}' not found in database.")
        except Product.MultipleObjectsReturned:
            print(f"⚠️ Multiple products found for '{name}', skipping.")
        except Exception as e:
            print(f"❌ Error updating {name}: {e}")

if __name__ == "__main__":
    main()
