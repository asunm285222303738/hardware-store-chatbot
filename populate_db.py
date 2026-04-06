import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hardware_store.settings')
django.setup()

from chatbot.models import Product

def populate():
    products = [
        {
            'name': 'Titanium Claw Hammer',
            'description': 'High-end titanium hammer with a sleek black grip. Engineered for balance and reduced fatigue.',
            'price': 1299.00,
            'stock_quantity': 20,
            'discount': 0.00,
        },
        {
            'name': 'Brushless Impact Drill',
            'description': 'Modern professional cordless impact drill. High torque and long battery life for heavy construction.',
            'price': 14999.00,
            'stock_quantity': 8,
            'discount': 800.00,
        },
        {
            'name': 'Magnetic Tape Measure',
            'description': 'Professional-grade heavy duty yellow tape measure with magnetic tip and auto-locking mechanism.',
            'price': 1999.00,
            'stock_quantity': 45,
            'discount': 0.00,
        },
        {
            'name': 'Workbench Vise',
            'description': 'Heavy iron workbench vise with steel handle. Essential for any serious workshop or garage.',
            'price': 6499.00,
            'stock_quantity': 3,
            'discount': 400.00,
        },
        {
            'name': 'Precision Laser Level 360°',
            'description': 'Self-leveling cross line laser with high visibility green beam. 360-degree coverage for precise layout.',
            'price': 19999.00,
            'stock_quantity': 10,
            'discount': 0.00,
        },
        {
            'name': 'Pro Safety Gear Set',
            'description': 'Full arrangement of safety glasses, ear muffs, and N95 masks for complete protection on-site.',
            'price': 3499.00,
            'stock_quantity': 15,
            'discount': 0.00,
        },
        {
            'name': 'Engineer\'s Scale Ruler',
            'description': 'Precision metal architectural scale ruler. High-quality markings for accurate design and engineering.',
            'price': 999.00,
            'stock_quantity': 25,
            'discount': 0.00,
        }
    ]

    for p_data in products:
        p, created = Product.objects.update_or_create(
            name=p_data['name'], 
            defaults=p_data
        )
        if created:
            print(f"Created product: {p.name}")
        else:
            print(f"Updated product: {p.name}")

if __name__ == "__main__":
    populate()
