from django.urls import path
from main.views import (
    show_main,
    show_products_xml, show_products_json, show_product_by_id_xml, show_product_by_id_json,
    product_list, product_detail, add_product, edit_product, delete_product,
    register_user, login_user, logout_user,
)

app_name = 'main'

urlpatterns = [
    # Authorization and main views
    path('', show_main, name='show_main'),
    path('register/', register_user, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    # Product views
    path('products/', product_list, name='product_list'),
    path('products/<int:id>/', product_detail, name='product_detail'),
    path('products/add/', add_product, name='add_product'),
    path('products/<int:id>/edit/', edit_product, name='edit_product'),
    path('products/<int:id>/delete/', delete_product, name='delete_product'),
    # Data delivery endpoints (public)
    path('xml/', show_products_xml, name='show_products_xml'),
    path('json/', show_products_json, name='show_products_json'),
    path('xml/<int:id>/', show_product_by_id_xml, name='show_product_by_id_xml'),
    path('json/<int:id>/', show_product_by_id_json, name='show_product_by_id_json'),
]