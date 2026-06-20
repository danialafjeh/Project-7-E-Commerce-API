from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('api/login', TokenObtainPairView.as_view(), name='users_login'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='users_token_refresh'),
    path('api/token/verify', TokenVerifyView.as_view(), name='users_token_verify'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'))
]

router = DefaultRouter()
router.register(r'api/users', views.UserAPI, basename='users_endpoints')
router.register(r'api/products', views.ProductAPI, basename='products_endpoints')
router.register(r'api/carts', views.CartAPI, basename='shopping_carts_endpoints')
router.register(r'api/addresses', views.AddressAPI, basename='users_addresses_endpoints')
router.register(r'api/orders', views.OrderAPI, basename='orders_endpoints')
urlpatterns += router.urls