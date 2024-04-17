from .models import *
from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer
    # order_items = serializers.PrimaryKeyRelatedField(many=True, 
    #                                                  queryset=OrderItem.objects.all())
    class Meta:
        model = Customer
        fields = [
            'user', 
            # 'order_items',
            ]

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    class Meta:
        model = Product
        fields = [
            'name',
            'describtion',
            'quantity',
            'brand_key',
            'price1',
            'price2',
            'image',
            'category',
            'id',
            ]
        
class OrderSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer
    order_items = serializers.PrimaryKeyRelatedField(many=True, queryset=Order.objects.all())
    class Meta:
        model = Order
        fields = [
            'customer',
            'date_ordered',
            'complete',
            'transaction_id',
            'order_items',
        ]

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer
    # order = OrderSerializer
    order = serializers.ReadOnlyField(source='order.customer.user.name')
    status = StatusSerializer
    class Meta:
        model = OrderItem
        fields = [
            'product',
            'order',
            'quantity',
            'date_added',
            'date_canceled',
            'status',
        ]

class ShippingAddressSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer
    order = OrderSerializer
    class Meta:
        model = ShippingAddress
        fields = [
            'customer',
            'order',
            'governerate',
            'city',
            'address',
            'landmark',
            'notes',
            'delivery_instruction',
            'date_added',
        ]

class FavItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer
    customer = CustomerSerializer
    class Meta:
        model = FavItem
        fields = [
            'product',
            'customer'
        ]