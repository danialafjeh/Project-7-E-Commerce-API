from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db import transaction
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.pagination import PageNumberPagination
from .models import Product, Cart, CartItem, UserAddress, Order, OrderItem
from .serializers import (
    UserReadSerializer,
    UserWriteSerializer,
    ProductReadSerializer,
    ProductWriteSerializer,
    CartSerializer,
    CartItemWriteSerializer,
    AddressSerializer,
    OrderSerializer
)

# Create your views here.

class UserAPI(ModelViewSet):
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['username']
    ordering_fields = ['date_joined']

    def get_queryset(self):
        if self.action in ['retrieve','partial_update','update']:
            return User.objects.filter(id=self.request.user.id)
        else:
            return User.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return UserWriteSerializer
        else:
            return UserReadSerializer
        
    def get_permissions(self):
        if self.action in ['list','destroy']:
            permissions = [IsAuthenticated, IsAdminUser]
        elif self.action in ['retrieve','partial_update','update']:
            permissions = [IsAuthenticated]
        elif self.action == 'create':
            permissions = [AllowAny]
        
        return [permission() for permission in permissions]
        


class ProductAPI(ModelViewSet):
    parser_classes = [MultiPartParser, FormParser]
    
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['name','brand__name','category__name']
    filterset_fields = ['category','brand']
    ordering_fields = ['price','created_at','updated_at']

    queryset = Product.objects.all()

    def get_serializer_class(self):
        if self.action in ['create','update','partial_update']:
            return ProductWriteSerializer
        else:
            return ProductReadSerializer
        
    def get_permissions(self):
        if self.action in ['list','retrieve']:
            permissions = [AllowAny]
        else:
            permissions = [IsAuthenticated, IsAdminUser]

        return [permission() for permission in permissions]



class CartAPI(ViewSet):
    def get_permissions(self):
        if self.action in ['list','search']:
            permissions = [IsAuthenticated, IsAdminUser]
        elif self.action in ['retrieve','add_item','delete_item']:
            permissions = [IsAuthenticated]

        return [permission() for permission in permissions]

    def list(self, request):
        queryset = Cart.objects.all()
        #serializer = CartSerializer(instance=queryset, many=True)
        #return Response(serializer.data, status=status.HTTP_200_OK)
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = CartSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    def retrieve(self, request, pk):
        instance = get_object_or_404(Cart, id=pk, user=request.user)
        serializer = CartSerializer(instance=instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        username = request.query_params.get('username')
        queryset = Cart.objects.filter(user__username__icontains=username)
        #serializer = CartSerializer(instance=queryset, many=True)
        #return Response(serializer.data, status=status.HTTP_200_OK)
        paginator = PageNumberPagination()
        page = paginator.paginate_queryset(queryset, request)
        serializer = CartSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def add_item(self, request):
        serializer = CartItemWriteSerializer(data=request.data)
        if serializer.is_valid():
            user_cart = get_object_or_404(Cart, user=request.user)

            product = serializer.validated_data['product']
            quantity = serializer.validated_data['quantity']

            existing_item = CartItem.objects.filter(cart=user_cart, product=product).first()

            if existing_item:
                existing_item.quantity += quantity
                existing_item.save()
                return Response({'message':'Item quantity updated'}, status=status.HTTP_200_OK)
            
            serializer.validated_data['cart'] = user_cart
            serializer.save()
            return Response({'message':'Item added to you cart'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['delete'], url_path=r'delete_item/(?P<pk>\d+)')
    def delete_item(self, request, pk):
        item = get_object_or_404(CartItem, id=pk, cart__user=request.user)
        item.delete()
        return Response({'message':'Item removed from your cart'}, status=status.HTTP_200_OK)

        

class AddressAPI(ModelViewSet):
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['user__username','city','province']
    ordering_fields = ['id','zipcode','city','province']

    def get_queryset(self):
        if self.action in ['retrieve','update','partial_update','destroy']:
            return UserAddress.objects.filter(user=self.request.user)
        else:
            return UserAddress.objects.all()
        
    serializer_class = AddressSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_permissions(self):
        if self.action == 'list':
            permissions = [IsAuthenticated, IsAdminUser]
        else:
            permissions = [IsAuthenticated]

        return [permission() for permission in permissions]



class OrderAPI(ViewSet):
    def get_permissions(self):
        if self.action in ['list','search','change_status']:
            permissions = [IsAuthenticated, IsAdminUser]
        else:
            permissions = [IsAuthenticated]

        return [permission() for permission in permissions]
        
    def list(self, request):
        queryset = Order.objects.all()
        #serializer = OrderSerializer(instance=queryset, many=True)
        #return Response(serializer.data, status=status.HTTP_200_OK)
        paginator = PageNumberPagination()
        page = paginator.paginate_queryset(queryset, request)
        serializer = OrderSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    def retrieve(self, request, pk):
        instance = get_object_or_404(Order, id=pk, user=request.user)
        serializer = OrderSerializer(instance=instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        username = request.query_params.get('username')
        queryset = Order.objects.filter(user__username__icontains=username)
        #serializer = OrderSerializer(instance=queryset, many=True)
        #return Response(serializer.data, status=status.HTTP_200_OK)
        paginator = PageNumberPagination()
        page = paginator.paginate_queryset(queryset, request)
        serializer = OrderSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    @action(detail=True, methods=['patch'])
    def change_status(self, request, pk):
        order = get_object_or_404(Order, id=pk)
        new_status = request.data.get('status')

        valid_statuses = [
            key for key, label in Order.status_choices
        ]
        if new_status not in valid_statuses:
            return Response({'message':'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)

        order.status = new_status
        order.save()
        return Response({'message':'Order status has been changed'}, status=status.HTTP_200_OK)
    
    @transaction.atomic
    @action(detail=False, methods=['post'])
    def checkout(self, request):
        user_cart = get_object_or_404(Cart, user=request.user)
        user_cart_items = CartItem.objects.filter(cart=user_cart)
        
        if not user_cart_items.exists():
            return Response({'message':'Your shopping cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

        address_id = request.data.get('address')
        address = get_object_or_404(UserAddress, id=address_id, user=request.user)
        delivery_method = request.data.get('delivery_method')

        if not delivery_method:
            return Response({'message':'Delivery method is required'}, status=status.HTTP_400_BAD_REQUEST)

        for item in user_cart_items:
            if item.quantity > item.product.stock_quantity:
               return Response({'message':f'Not enough stock for {item.product.name}'}, status=status.HTTP_400_BAD_REQUEST)

        new_order = Order.objects.create(
            user = request.user,
            address = address,
            delivery_method = delivery_method,
        )
        
        for item in user_cart_items:
            if item.product.is_sale:
                price = item.product.sale_price
            else:
                price = item.product.price
            
            OrderItem.objects.create(
                order = new_order,
                product = item.product,
                price = price,
                quantity = item.quantity,
            )

            item.product.stock_quantity -= item.quantity
            item.product.save()

        user_cart_items.delete()
        return Response({'message':'Your order has been registered'}, status=status.HTTP_201_CREATED)
            

    
