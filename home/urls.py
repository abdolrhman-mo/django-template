from . import views
from django.urls import path

app_name = 'store'

urlpatterns = [
    path('', views.home, name="home"),
    path('company_page/', views.companyPage, name="companyPage"),
    path('cart/', views.cart, name="cart"),
    path('add/<int:product_id>/', views.add_to_cart, name="add_to_cart"),
    path('remove/<int:item_id>/', views.remove_from_cart, name="remove_from_cart"),
    path('profile/', views.profile, name="profile"),
    path('contact/', views.cart, name="contact"),
    path('products/', views.cart, name="products"),
    path('checkout/', views.checkout, name="checkout"),
    path('add_address/', views.AddAddress.as_view(), name="add_address"),
    path('edit_address/<int:address_id>', views.edit_address, name="edit_address"),
    path('remove_address/<int:address_id>', views.RemoveAddress.as_view(), name="remove_address"),
    path('purchase/', views.purchase, name="purchase"),
    path('cancel_order/<int:order_id>', views.cancel_order, name="cancel_order"),

    path('login/', views.user_login, name='login'),
    path('signup/', views.user_signup, name='signup'),
    path('logout/', views.user_logout, name='logout'),
    
    path('api/products', views.getProducts, name="products_api"),
]
