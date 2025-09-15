from django.urls import path
from main.views import show_main, show_products_xml, show_products_json, show_product_by_id_xml, show_product_by_id_json, product_list, product_detail, add_product

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('xml/', show_products_xml, name='show_products_xml'),
    path('json/', show_products_json, name='show_products_json'),
    path('xml/<int:id>/', show_product_by_id_xml, name='show_product_by_id_xml'),
    path('json/<int:id>/', show_product_by_id_json, name='show_product_by_id_json'),
    path('products/', product_list, name='product_list'),
    path('products/add/', add_product, name='add_product'),
    path('products/<int:id>/', product_detail, name='product_detail'),
]