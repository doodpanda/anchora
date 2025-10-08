from django.urls import path
from main.views import (
    show_main,
    show_products_xml, show_products_json, show_product_by_id_xml, show_product_by_id_json,
    product_list, product_detail, add_product, edit_product, delete_product,
    register_user, login_user, logout_user,
    get_products_json, get_product_detail_json, create_product_ajax, update_product_ajax, delete_product_ajax,
    login_ajax, register_ajax, logout_ajax,
)

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('register/', register_user, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('products/', product_list, name='product_list'),
    path('products/<int:id>/', product_detail, name='product_detail'),
    path('products/add/', add_product, name='add_product'),
    path('products/<int:id>/edit/', edit_product, name='edit_product'),
    path('products/<int:id>/delete/', delete_product, name='delete_product'),
    path('xml/', show_products_xml, name='show_products_xml'),
    path('json/', show_products_json, name='show_products_json'),
    path('xml/<int:id>/', show_product_by_id_xml, name='show_product_by_id_xml'),
    path('json/<int:id>/', show_product_by_id_json, name='show_product_by_id_json'),
    path('api/products/', get_products_json, name='get_products_json'),
    path('api/products/<int:id>/', get_product_detail_json, name='get_product_detail_json'),
    path('api/products/create/', create_product_ajax, name='create_product_ajax'),
    path('api/products/<int:id>/update/', update_product_ajax, name='update_product_ajax'),
    path('api/products/<int:id>/delete/', delete_product_ajax, name='delete_product_ajax'),
    path('api/login/', login_ajax, name='login_ajax'),
    path('api/register/', register_ajax, name='register_ajax'),
    path('api/logout/', logout_ajax, name='logout_ajax'),
]