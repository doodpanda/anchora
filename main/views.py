from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.http import HttpRequest as Request
from django.core import serializers
from django.db.models import Q
from .models import Product

from .forms import ProductForm, CustomUserCreationForm, CustomAuthenticationForm
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone

# Create your views here.
def show_main(request: Request) -> HttpResponse:
    products = Product.objects.filter(is_blacklisted=False)
    
    context = {
        'products': products
    }
    if request.user.is_authenticated:
        context['username'] = request.user.username
        context['last_login'] = request.COOKIES.get('last_login')
    return render(request,'main.html', context)

# List user's own products (requires login)
@login_required(login_url='main:login')
def product_list(request):
    products = Product.objects.filter(user=request.user)
    return render(request, 'product_list.html', {'products': products})

# Product detail page (public access, but blacklisted products only visible to owner)
def product_detail(request, id):
    product = get_object_or_404(Product, pk=id)
    
    # If product is blacklisted, only show to the owner
    if product.is_blacklisted and (not request.user.is_authenticated or product.user != request.user):
        from django.http import Http404
        raise Http404("Product not found")
    
    return render(request, 'product_detail.html', {'product': product})

# Add product form page
@login_required(login_url='main:login')
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.save()
            return redirect(reverse('main:product_list'))
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})

# Edit product form page (owner only)
@login_required(login_url='main:login')
def edit_product(request, id):
    product = get_object_or_404(Product, pk=id, user=request.user)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f'Product "{product.name}" has been updated successfully.')
            return redirect('main:product_detail', id=product.id)
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'edit_product.html', {'form': form, 'product': product})

# Delete product (owner only)
@login_required(login_url='main:login')
def delete_product(request, id):
    product = get_object_or_404(Product, pk=id, user=request.user)
    
    if request.method == 'POST':
        product_name = product.name
        product.delete()
        messages.success(request, f'Product "{product_name}" has been deleted successfully.')
        return redirect('main:product_list')
    
    return render(request, 'delete_product.html', {'product': product})

# View: All Products as XML (public)
def show_products_xml(request):
    data = Product.objects.all()
    return HttpResponse(serializers.serialize('xml', data), content_type='application/xml')

# View: All Products as JSON (public)
def show_products_json(request):
    data = Product.objects.all()
    return HttpResponse(serializers.serialize('json', data), content_type='application/json')

# View: Product by ID as XML (public)
def show_product_by_id_xml(request, id):
    data = Product.objects.filter(pk=id)
    return HttpResponse(serializers.serialize('xml', data), content_type='application/xml')

# View: Product by ID as JSON (public)
def show_product_by_id_json(request, id):
    data = Product.objects.filter(pk=id)
    return HttpResponse(serializers.serialize('json', data), content_type='application/json')


def register_user(request: Request) -> HttpResponse:
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully. Please log in.')
            return redirect('main:login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


def login_user(request: Request) -> HttpResponse:
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                response = redirect('main:show_main')
                response.set_cookie('last_login', str(timezone.now()))
                return response
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_user(request: Request) -> HttpResponse:
    logout(request)
    response = redirect('main:login')
    response.delete_cookie('last_login')
    return response