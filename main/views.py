from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.http import HttpRequest as Request
from django.core import serializers
from .models import Product

from .forms import ProductForm
from django.urls import reverse
from django.shortcuts import redirect

# Create your views here.
def show_main(request: Request) -> HttpResponse:
    # directly render the main.html template without any context
    return render(request,'main.html')

# List all products with Add and Detail buttons
def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

# Product detail page
def product_detail(request, id):
    product = get_object_or_404(Product, pk=id)
    return render(request, 'product_detail.html', {'product': product})

# Add product form page
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('main:product_list'))
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})

# View: All Products as XML
def show_products_xml(request):
    data = Product.objects.all()
    return HttpResponse(serializers.serialize('xml', data), content_type='application/xml')

# View: All Products as JSON
def show_products_json(request):
    data = Product.objects.all()
    return HttpResponse(serializers.serialize('json', data), content_type='application/json')

# View: Product by ID as XML
def show_product_by_id_xml(request, id):
    data = Product.objects.filter(pk=id)
    return HttpResponse(serializers.serialize('xml', data), content_type='application/xml')

# View: Product by ID as JSON
def show_product_by_id_json(request, id):
    data = Product.objects.filter(pk=id)
    return HttpResponse(serializers.serialize('json', data), content_type='application/json')