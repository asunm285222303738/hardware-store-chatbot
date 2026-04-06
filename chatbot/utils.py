from .models import Product
from django.db.models import Q

def find_products(query):
    """
    Simple rule-based NLP to find products based on user query.
    It searches for keywords in product names and descriptions.
    """
    if not query:
        return []
    
    # Predefined keywords mapping (optional enhancement)
    # keywords = query.lower().split()
    
    # Search in Name and Description
    products = Product.objects.filter(
        Q(name__icontains=query) | Q(description__icontains=query)
    )
    
    return products
