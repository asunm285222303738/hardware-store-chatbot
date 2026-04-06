from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Product, Order
from .utils import find_products
import json

def home(request):
    """Renders the chatbot landing page interface."""
    return render(request, 'chatbot/home.html')

def products_list(request):
    """Shows all available products from the database."""
    products = Product.objects.all()
    return render(request, 'chatbot/products.html', {'products': products})

@csrf_exempt
def chatbot_api(request):
    """
    API endpoint that receives user message as JSON and returns a text reply 
    along with any matching products.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_query = data.get('query', '').strip()

            if not user_query:
                return JsonResponse({'response': "Please specify a product you're looking for or ask a question."})

            # Rule-based search logic
            found_products = find_products(user_query)

            if found_products.exists():
                product_data = []
                for p in found_products:
                    product_data.append({
                        'id': p.id,
                        'name': p.name,
                        'price': str(p.price),
                        'stock': p.stock_quantity,
                        'image': p.image.url if p.image else 'https://via.placeholder.com/150',
                        'sku': f"SKU: {p.id:03d}-HP"
                    })

                return JsonResponse({
                    'response': f"Great! I found {found_products.count()} matching products for your project.",
                    'products': product_data
                })
            else:
                return JsonResponse({'response': "I couldn't find any products matching your query. Would you like to check our full catalog or ask something else?"})

        except Exception as e:
            return JsonResponse({'error': f"Processing error: {str(e)}"}, status=500)

    return JsonResponse({'error': 'Invalid request method. Please use POST.'}, status=400)


def buy_product(request):
    """Handles the creation of orders when a user clicks 'Buy Now'."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            product_id = data.get('product_id')
            quantity = int(data.get('quantity', 1))
            
            product = get_object_or_404(Product, id=product_id)
            
            if product.stock_quantity < quantity:
                return JsonResponse({'error': 'Insufficient stock available.'}, status=400)
            
            total_price = product.price * quantity
            order = Order.objects.create(
                product=product,
                quantity=quantity,
                total_price=total_price,
                status='Confirmed'
            )
            
            # Decrement stock
            product.stock_quantity -= quantity
            product.save()
            
            return JsonResponse({
                'message': 'Order confirmed successfully!',
                'order_id': order.id,
                'total_price': str(total_price)
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
            
    return JsonResponse({'error': 'Invalid request'}, status=400)

def orders_history(request):
    """Simple view for order history."""
    orders = Order.objects.all().order_by('-order_date')
    return render(request, 'chatbot/orders.html', {'orders': orders})

def contact(request):
    """Basic contact page."""
    return render(request, 'chatbot/contact.html')
