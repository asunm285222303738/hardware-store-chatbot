from django.urls import path
from . import views

urlpatterns = [
    path('chatbot/', views.home, name='home'),
    path('products/', views.products_list, name='products'),
    path('api/chatbot/', views.chatbot_api, name='chatbot_api'),
    path('api/buy/', views.buy_product, name='buy_product'),
    path('orders/', views.orders_history, name='orders'),
    path('contact/', views.contact, name='contact'),
]
