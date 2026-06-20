from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=150)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name
    
class Brand(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    image = models.ImageField(upload_to='upload/products', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True, related_name='products')
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, blank=True, null=True, related_name='products')
    price = models.DecimalField(default=0, decimal_places=0, max_digits=12)
    is_sale = models.BooleanField(default=False)
    sale_price =  models.DecimalField(decimal_places=0, max_digits=12, blank=True, null=True)
    stock_quantity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at =  models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Shopping cart for user: {self.user.username}'
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
       unique_together = ('cart', 'product')

    def __str__(self):
        return f'Product: {self.product.name} in {self.cart}'
    
class UserAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    city = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=10)
    full_address = models.TextField()

    class Meta:
        verbose_name_plural = 'Addresses'

    def __str__(self):
        return f'Shipping address for user: {self.user.username}'
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    address = models.ForeignKey(UserAddress, on_delete=models.CASCADE, related_name='orders')
    delivery_choices = [
        ('POST', 'Post Office'),
        ('FAST', 'Fast Shipping'),
    ]
    delivery_method = models.CharField(max_length=50, choices=delivery_choices)
    status_choices = [
        ('WAITING', 'Waiting for payment'),
        ('PREPARING', 'Making things ready'),
        ('SHIPPING', 'On the way'),
        ('DELIVERED', 'Delivered'),
        ('CANCELED', 'Canceled')
    ]
    status = models.CharField(max_length=50, choices=status_choices, default='WAITING')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Order #{self.id} for user: {self.user.username}'
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(default=0, decimal_places=0, max_digits=12)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Product: {self.product.name} in {self.order}'

