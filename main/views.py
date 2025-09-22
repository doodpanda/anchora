from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.http import HttpRequest as Request
from django.core import serializers
from .models import Product

from .forms import ProductForm
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone

# Create your views here.
def show_main(request: Request) -> HttpResponse:
    context = {}
    if request.user.is_authenticated:
        context['username'] = request.user.username
        context['last_login'] = request.COOKIES.get('last_login')
    return render(request,'main.html', context)

# List all products with Add and Detail buttons
@login_required(login_url='main:login')
def product_list(request):
    products = Product.objects.filter(user=request.user)
    return render(request, 'product_list.html', {'products': products})

# Product detail page
@login_required(login_url='main:login')
def product_detail(request, id):
    product = get_object_or_404(Product, pk=id, user=request.user)
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

# View: All Products as XML
def show_products_xml(request):
    data = Product.objects.filter(user=request.user) if request.user.is_authenticated else Product.objects.none()
    return HttpResponse(serializers.serialize('xml', data), content_type='application/xml')

# View: All Products as JSON
def show_products_json(request):
    data = Product.objects.filter(user=request.user) if request.user.is_authenticated else Product.objects.none()
    return HttpResponse(serializers.serialize('json', data), content_type='application/json')

# View: Product by ID as XML
def show_product_by_id_xml(request, id):
    data = Product.objects.filter(pk=id, user=request.user) if request.user.is_authenticated else Product.objects.none()
    return HttpResponse(serializers.serialize('xml', data), content_type='application/xml')

# View: Product by ID as JSON
def show_product_by_id_json(request, id):
    data = Product.objects.filter(pk=id, user=request.user) if request.user.is_authenticated else Product.objects.none()
    return HttpResponse(serializers.serialize('json', data), content_type='application/json')


def register_user(request: Request) -> HttpResponse:
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully. Please log in.')
            return redirect('main:login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


def login_user(request: Request) -> HttpResponse:
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                response = redirect('main:show_main')
                response.set_cookie('last_login', timezone.now().strftime('%Y-%m-%d %H:%M:%S'))
                return response
        messages.error(request, 'Invalid username or password')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_user(request: Request) -> HttpResponse:
    logout(request)
    response = redirect('main:login')
    response.delete_cookie('last_login')
    return response