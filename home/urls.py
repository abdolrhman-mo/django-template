from . import views
from django.urls import path, include
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'customers', views.CustomerViewSet)
router.register(r'categories', views.CategoryViewSet)
# router.register(r'products', views.ProductViewSet)
# router.register(r'products', views.MyProductList.as_view(), basename='MyProducts')
# router.register(r'products', views.getProducts)
# router.register(r'products/<str:pk>', views.getProduct)
router.register(r'orders', views.OrderViewSet)
router.register(r'statuses', views.StatusViewSet)
# router.register(r'order_items', views.OrderItemViewSet)
router.register(r'shipping_addresses', views.ShippingAddressViewSet)
router.register(r'fav_items', views.FavItemViewSet)

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
    path('add_fav/<int:product_id>', views.AddFav.as_view(), name="add_fav"),
    path('remove_fav/<int:product_id>', views.RemoveFav.as_view(), name="remove_fav"),

    path('login/', views.user_login, name='login'),
    path('signup/', views.user_signup, name='signup'),
    path('logout/', views.user_logout, name='logout'),
    
    path('api/', include(router.urls)),
    path('api/products/', views.ProductList.as_view()),
    path('api/products/<int:pk>', views.ProductDetail.as_view()),
    path('api/users/<int:pk>', views.UserDetail.as_view()),
    path('api/order_items/', views.OrderItemList.as_view()),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

# the code below raises an error
# urlpatterns = format_suffix_patterns(urlpatterns)