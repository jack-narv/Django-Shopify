from django.urls import path
from .views import ProductView
from .views import ShopifyView
from .views import importarProductos
from .views import AtributosView
from .views import WebhooksView

urlpatterns=[
    path('products/', ProductView.as_view(),name='product_list'),
    path('products/<int:id>', ProductView.as_view(),name='product_process'),
    path('productosShopify/', ShopifyView.as_view(), name='product_list_shopify'),
    path('productosShopify/<int:id>', ShopifyView.as_view(), name='product_list_shopify_process'),
    path('importarProductos/', importarProductos.as_view(), name='import_products'),
    path('atributos/', AtributosView.as_view(), name='atributos_list'),
    path('atributos/<int:id>', AtributosView.as_view(), name='atributos_process'),
    path('webhooks/', WebhooksView.as_view(), name='webhooks_list')
]