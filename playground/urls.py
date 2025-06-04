from django.urls import path
from . import views

# URLConf
urlpatterns = [
    path('hello/', views.say_hello), # Test
    path('accueil/', views.accueil, name='accueil'),
    path('products/', views.products, name='products'),
    path('cart/', views.cart_detail),
    path('cart_add/<int:product_id>', views.cart_add, name='cart_add'),
    path('cart_remove/<int:product_id>', views.cart_remove, name='cart_remove'),
    path('cart_remove_one/<int:product_id>', views.cart_remove_one, name='cart_remove_one'),
    path('cart_detail/', views.cart_detail, name='cart_detail'),
    path('facture/<int:facture_id>', views.get_facture_by_id, name='facture'),
    path('factures/', views.factures, name='factures'),
    path('checkout/<str_products_ids>', views.checkout, name='checkout'),
]