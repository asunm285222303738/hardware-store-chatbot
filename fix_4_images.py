import os
import django
import requests
from django.core.files.base import ContentFile
import urllib.parse

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hardware_store.settings')
django.setup()

from chatbot.models import Product

def main():
    # Using much simpler single-word keywords without spaces to prevent LoremFlickr 404s
    products_to_update = {
        "Brushless Impact Drill": "drill",
        "Magnetic Tape Measure": "measure",
        "Precision Laser Level 360°": "laser",
        "Pro Safety Gear Set": "helmet"
    }
    
    for name, keyword in products_to_update.items():
        try:
            product = Product.objects.get(name__iexact=name)
            
            # Simple keyword url
            url = f"https://loremflickr.com/400/400/{urllib.parse.quote(keyword)}"
            
            print(f"Downloading image for '{name}' using string '{keyword}'... (URL: {url})")
            response = requests.get(url, timeout=10)
            
            safe_name = name.replace(' ', '_').replace('°', '').replace("'", "")
            file_name = f"{safe_name}.jpg"
                
            if response.status_code == 200:
                product.image.save(file_name, ContentFile(response.content), save=True)
                print(f"✅ Successfully added image to {name}.")
            else:
                print(f"❌ Failed to download from loremflickr. HTTP Status: {response.status_code}")
                print("Trying fallback to placehold.co...")
                
                # Fallback to pure placeholder if loremflickr fails on niche words
                fallback_url = f"https://placehold.co/400x400/e9ecef/495057/png?text={urllib.parse.quote(name)}"
                fb_resp = requests.get(fallback_url, timeout=10)
                if fb_resp.status_code == 200:
                    product.image.save(file_name, ContentFile(fb_resp.content), save=True)
                    print(f"✅ Added text-placeholder fallback for {name}.")
                else:
                    print("❌ Fallback also failed.")
                
        except Product.DoesNotExist:
            print(f"⚠️ Product '{name}' not found in database.")
        except Exception as e:
            print(f"❌ Error updating {name}: {e}")

if __name__ == "__main__":
    main()
