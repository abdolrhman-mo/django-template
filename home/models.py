from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.username
    
class Order(models.Model): # customer can have many orders
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.filter(status=Status.objects.get(name='cart'))
        total = sum([item.get_total for item in orderitems])
        return total
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.filter(status=Status.objects.get(name='cart'))
        total = sum([item.quantity for item in orderitems])
        return total
    
    def __str__(self):
        return "order " + str(self.id)

class Category(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name

class Product(models.Model):
    CHOICES = [
        ('1', 'sale'),
        ('2', 'out of stock')
    ]
    name = models.CharField(max_length=50)
    describtion = models.CharField(max_length=250)
    quantity = models.IntegerField(null=True)
    brand_key = models.IntegerField()
    price1 = models.IntegerField(null=True)
    price2 = models.IntegerField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)

    @property
    def imageUrl(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    
    # def get_quantity(self):
    #     s = 0
    #     for imported in ImportProduct.objects.filter(product=self.):
    #         s += imported.quantity
    #     return s
    
    def __str__(self):
        return self.name
        
class Status(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
class OrderItem(models.Model): # order can have many order items
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_canceled = models.DateTimeField(null=True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, null=True)
    
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total
    
    def __str__(self):
        return "order item: " + str(self.quantity) + " " + self.product.name

class ShippingAddress(models.Model):
    CHOICES = [
        ('1', 'Home (7am-9pm, all days)'),
        ('2', 'Office (9am-6pm, Weekdays)')
    ]
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    governerate = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    landmark = models.CharField(max_length=200, null=True)
    notes = models.CharField(max_length=500, null=True)
    delivery_instruction = models.CharField(choices=CHOICES, max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.address

class ImportProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    date_imported = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return "Import for " + self.product.name + " on " + self.date_imported.strftime('%d/%m/%y - %I:%M')
    
class ExportProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    date_exported = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return "Export for " + self.product.name + " on " + self.date_exported.strftime('%d/%m/%y - %I:%M')
    
class FavItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return self.customer.user.username + " loves " + self.product.name
    