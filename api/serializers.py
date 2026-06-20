from django.contrib.auth.models import User
from .models import Product, Cart, CartItem, UserAddress, Order, OrderItem
from rest_framework import serializers
 
class UserReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password','user_permissions','groups')

class UserWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password'
        )
        extra_kwargs = {
            'password':{
                'write_only':True
            },
            'first_name':{
                'required':True
            },
            'last_name':{
                'required':True
            },
            'email':{
                'required':True
            }
        }
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        Cart.objects.create(user=user)
        return user
    


class ProductReadSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    brand = serializers.SlugRelatedField(slug_field='name', read_only=True)
    class Meta:
        model = Product
        fields = '__all__'

class ProductWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
    


class CartItemWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'
        extra_kwargs = {
            'cart':{
                'read_only':True
            }
        }

class CartItemReadSerializer(serializers.ModelSerializer):
    #cart = serializers.StringRelatedField()
    product = serializers.SlugRelatedField(slug_field='name', read_only=True)
    class Meta:
        model = CartItem
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)
    items = CartItemReadSerializer(many=True, read_only=True)
    class Meta:
        model = Cart
        fields = '__all__'



class AddressSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)
    class Meta:
        model = UserAddress
        fields = '__all__'



class OrderItemReadSerializer(serializers.ModelSerializer):
    product = serializers.SlugRelatedField(slug_field='name', read_only=True)
    class Meta:
        model = OrderItem
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)
    address = serializers.SlugRelatedField(slug_field='full_address', read_only=True)
    items = OrderItemReadSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields ='__all__'