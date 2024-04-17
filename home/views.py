from .models import *
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout 
from .forms import SignupForm, LoginForm, AddressForm
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from datetime import datetime
from django.views import View
from .serializers import *
# request and response
from rest_framework.response import Response
# fun based views
from rest_framework.parsers import JSONParser
from django.views.decorators import csrf
from rest_framework.decorators import api_view
# class based views
from rest_framework.views import APIView
from rest_framework import status
from django.http import Http404
from rest_framework import mixins
from rest_framework import generics
# viewsets based views
from rest_framework import viewsets

def displaySessionCartItems(request):
    if "cart_items" not in request.session:
        request.session["cart_items"] = []
    items_id = request.session['cart_items']
    order = {'get_cart_items': 0, 'get_cart_total': 0}
    items = []
    for item_id in items_id:
        found = False
        for item in items:
            if item['id'] == item_id:
                item['quantity'] += 1
                order['get_cart_items'] += 1
                order['get_cart_total'] += Product.objects.get(id=item_id).price
                found = True
        if found == False:
            items.append({'id': item_id, 'quantity': 1, 'name': Product.objects.get(id=item_id).name})
            order['get_cart_items'] += 1
            order['get_cart_total'] += Product.objects.get(id=item_id).price
    context = {
        'items': items,
        'order': order,
    }
    return context

def add_to_cart_fun(request, selected_product):
    try:
        order_item = OrderItem.objects.get(
            product=selected_product,
            order=(Order.objects.get(customer=request.user.customer)),
            status=(Status.objects.get(name="cart"))
        )
        order_item.quantity += 1
        order_item.save()
    except:
        order_item = OrderItem(product=selected_product,
                    order=(Order.objects.get(customer=request.user.customer)), 
                    quantity=1, 
                    status=(Status.objects.get(name="cart")))
        order_item.save()

def add_fav_fun(request, selected_product):
    try:
        FavItem.objects.get(customer=Customer.objects.get(user=request.user),
                        product=selected_product)
    except:    
        FavItem(customer=Customer.objects.get(user=request.user),
                product=selected_product).save()


# @api_view(['GET'])
# def getProducts(request):
#     queryset = Product.objects.all()
#     serializer = ProductSerializer(queryset, many=True)
#     return Response(serializer.data)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

# class ProductList(APIView): 
#     def get(self, request, format=None):
#         products = Product.objects.all() 
#         serializer = ProductSerializer(products, many=True) # serialize a queryset
#         return Response(serializer.data)
    
#     def post(self, request, format=None):
#         serializer = ProductSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# class ProductList(mixins.ListModelMixin,
#                   mixins.CreateModelMixin,
#                   generics.GenericAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer

#     def get(self, request):
#         return self.list(request)

#     def post(self, request):
#         return self.create(request)

class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

# class ProductDetail(APIView):
#     def get_product(self, pk):
#         try:
#             return Product.objects.get(id=pk)
#         except:
#             raise Http404

#     def get(self, request, pk, format=None):
#         product = self.get_product(pk)
#         serializer = ProductSerializer(product) # serialize a model instance
#         return Response(serializer.data)
    
#     def put(self, request, pk, format=None):
#         product = self.get_product(pk)
#         serializer = ProductSerializer(product, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     def delete(self, request, pk, format=None):
#         product = self.get_product(pk)
#         product.delete()
#         return HttpResponse(status=status.HTTP_204_NO_CONTENT)

# class ProductDetail(mixins.RetrieveModelMixin,
#                     mixins.UpdateModelMixin,
#                     mixins.DestroyModelMixin,
#                     generics.GenericAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer

#     def get(self, request, pk):
#         return self.retrieve(request, pk)

#     def put(self, request, pk):
#         return self.update(request, pk)

#     def delete(self, request, pk):
#         return self.destroy(request, pk)

class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class StatusViewSet(viewsets.ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer

# class OrderItemViewSet(viewsets.ModelViewSet):
#     queryset = OrderItem.objects.all()
#     serializer_class = OrderItemSerializer

class OrderItemList(generics.ListCreateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    
    # order_items are related with the user who creates them
    def perform_create(self, serializer):
        serializer.save(order=Order.objects.get(user=self.request.user))

class ShippingAddressViewSet(viewsets.ModelViewSet):
    queryset = ShippingAddress.objects.all()
    serializer_class = ShippingAddressSerializer

class FavItemViewSet(viewsets.ModelViewSet):
    queryset = FavItem.objects.all()
    serializer_class = FavItemSerializer

def home(request):
    # QUANTITY OF ALL PRODUCTS AFTER IMPORTS & EXPORTS
    for product in Product.objects.all():
        s = 0
        for imported in ImportProduct.objects.filter(product=product):
            s += imported.quantity
        for exported in ExportProduct.objects.filter(product=product):
            s -= exported.quantity
        product.quantity = s
        product.save()
    #############################
    if request.user.is_authenticated:
        try:
            c = Customer.objects.get(user=request.user)
        except:
            c = Customer(user=request.user)
            c.save()
        # customer, created = Order.objects.get_or_create(customer=customer, complete=False)
        if "cart_items" in request.session:
            for cart_item_id in request.session['cart_items']:
                add_to_cart_fun(request, Product.objects.get(id=cart_item_id))
            del request.session['cart_items']
        if "fav_items" in request.session:
            for fav_item_id in request.session['fav_items']:
                add_fav_fun(request, Product.objects.get(id=fav_item_id))
            del request.session['fav_items']
    else:
        if "cart_items" not in request.session:
            request.session["cart_items"] = []
        if "fav_items" not in request.session:
            request.session["fav_items"] = []

    products = Product.objects.all()
    context = {
        'products': products,
    }
    return render(request, "home/index.html", context)

def companyPage(request):
    products = Product.objects.all()
    orders = Order.objects.all()
    context = {
        'products': products,
        'orders': orders,
    }
    return render(request, "home/companyPage.html", context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, 
                                                     complete=False)
        # items = order.orderitem_set.all()
        items = order.orderitem_set.filter(status=Status.objects.get(name="cart"))
        context = {
            'items': items,
            'order': order,
            'items_count': items.count(),
        }
    else:
        context = displaySessionCartItems(request)

    return render(request, 'home/cart.html', context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, 
                                                     complete=False)
        # items = order.orderitem_set.all()
        items = order.orderitem_set.filter(status=Status.objects.get(name="cart"))
        addresses = ShippingAddress.objects.filter(customer=Customer.objects.get(user=request.user))
    else:
        # items = []
        return redirect('store:login')
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            new_address = ShippingAddress(governerate=form.cleaned_data['governerate'],
                                        city=form.cleaned_data['city'],
                                        address=form.cleaned_data['address'],
                                        landmark=form.cleaned_data['landmark'],
                                        notes=form.cleaned_data['notes'],
                                        delivery_instruction=form.cleaned_data['delivery_instruction'],
                                        customer=Customer.objects.get(user=request.user))
            new_address.save()

            # return AddressForm('store:checkout')
            return HttpResponseRedirect("/checkout")
    else:
        form = AddressForm()
    context = {
        'items': items,
        'order': order,
        'addresses': addresses,
        'form': form,

    }
    return render(request, 'home/checkout.html', context)

def add_address(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.cleaned_data['address']
            a = ShippingAddress(address=address)
            a.save()
            return HttpResponseRedirect("/checkout")
    else:
        form = AddressForm()
    context = {
        'form': form,
    }
    return render(request, 'home/addAddress.html', context)

class AddAddress(View):
    form_class = AddressForm
    initial = {}
    template_name = "home/addAddress.html"

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            a = ShippingAddress(customer=Customer.objects.get(user=request.user),
                                address=form.cleaned_data['address'], 
                                governerate=form.cleaned_data['governerate'], 
                                city=form.cleaned_data['city'])
            a.save()
            return HttpResponseRedirect("/checkout")
        
        return render(request, self.template_name, {'form': form})
    
class RemoveAddress(View):
    def get(self, request, address_id):
        ShippingAddress.objects.get(id=address_id).delete()
        return HttpResponseRedirect(f"/checkout")

def edit_address(request, address_id):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.cleaned_data['address']
            a = ShippingAddress.objects.get(id=address_id)
            a.address=address
            a.save()
            return HttpResponseRedirect("/checkout")
    else:
        s = ShippingAddress.objects.get(id=address_id)
        form = AddressForm(initial={"address": s.address, "governerate": s.governerate, "city": s.city})
    context = {
        'form': form,
    }
    return render(request, 'home/editAddress.html', context)

def add_to_cart(request, product_id):
    selected_product = Product.objects.get(id=product_id)
    if request.user.is_authenticated:
        add_to_cart_fun(request, selected_product)
    else:
        request.session["cart_items"] += [selected_product.id]

    return redirect('store:home')

def remove_from_cart(request, item_id):
    if request.user.is_authenticated:
        OrderItem.objects.get(id=item_id).delete()
    else:
        new_cart_items = []
        for cart_item in request.session['cart_items']:
            if cart_item != item_id:
                new_cart_items += [cart_item]
        request.session['cart_items'] = new_cart_items
            
    return redirect('store:cart')

def profile(request):
    ordered = OrderItem.objects.filter(status=Status.objects.get(name='ordered'))
    canceled = OrderItem.objects.filter(status=Status.objects.get(name='canceled'))
    not_dispatched = OrderItem.objects.filter(status=Status.objects.get(name='not yet dispatched'))
    context = {
        'ordered': ordered,
        'canceled': canceled,
        'not_dispatched': not_dispatched,
    }
    return render(request, 'home/profile.html', context)

def purchase(request):
    cart_items = OrderItem.objects.filter(status=Status.objects.get(name="cart"))
    for cart_item in cart_items:
        cart_item.status = Status.objects.get(name="not yet dispatched")
        cart_item.date_added = datetime.now()
        cart_item.save()
    # EXPORT PRODUCTS
    for cart_item in cart_items:
        e = ExportProduct(product=Product.objects.get(name=cart_item.product.name), 
                      quantity=cart_item.quantity)
        e.save()
    #####################
    return redirect('store:profile')

def cancel_order(request, order_id):
    canceled_order = OrderItem.objects.get(id=order_id) 
    canceled_order.status = Status.objects.get(name="canceled")
    canceled_order.date_canceled = datetime.now()
    canceled_order.save()
    return redirect('store:profile')

class AddFav(View):
    def get(self, request, product_id):
        selected_product = Product.objects.get(id=product_id)
        if request.user.is_authenticated:
            add_fav_fun(request, selected_product)
        else:
            # check if selected product in 'fav_items'
            found = False
            for item_id in request.session['fav_items']:
                if item_id == selected_product.id:
                    found = True
                    break
            if found == False:
                request.session['fav_items'] += [selected_product.id]
        return HttpResponseRedirect("/")

class RemoveFav(View):
    def get(self, request, product_id):
        if request.user.is_authenticated:
            FavItem.objects.get(customer=Customer.objects.get(user=request.user),
                                product=Product.objects.get(id=product_id)).delete()
        else:
            new_fav_items = []
            for fav_item in request.sessions['fav_items']:
                if fav_item != product_id:
                    new_fav_items += [fav_item]
            request.sessions['fav_items'] = new_fav_items

        return HttpResponseRedirect("/")

def user_signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('store:login')
    else:
        form = SignupForm()
    return render(request, 'home/signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)    
                return redirect('store:home')
    else:
        form = LoginForm()
    return render(request, 'home/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('store:login')