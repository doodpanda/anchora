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

def show_main(request: Request) -> HttpResponse:
    context = {}
    if request.user.is_authenticated:
        context['username'] = request.user.username
        context['last_login'] = request.COOKIES.get('last_login')
    return render(request,'main_ajax.html', context)

@login_required(login_url='main:login')
def product_list(request):
    products = Product.objects.filter(user=request.user)
    return render(request, 'product_list_ajax.html', {'products': products})

def product_detail(request, id):
    product = get_object_or_404(Product, pk=id)
    
    if product.is_blacklisted and (not request.user.is_authenticated or product.user != request.user):
        from django.http import Http404
        raise Http404("Product not found")
    
    return render(request, 'product_detail_ajax.html', {'product': product})

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

@login_required(login_url='main:login')
def delete_product(request, id):
    product = get_object_or_404(Product, pk=id, user=request.user)
    
    if request.method == 'POST':
        product_name = product.name
        product.delete()
        messages.success(request, f'Product "{product_name}" has been deleted successfully.')
        return redirect('main:product_list')
    
    return render(request, 'delete_product.html', {'product': product})

def show_products_xml(request):
    data = Product.objects.all()
    return HttpResponse(serializers.serialize('xml', data), content_type='application/xml')

def show_products_json(request):
    data = Product.objects.all()
    return HttpResponse(serializers.serialize('json', data), content_type='application/json')

def show_product_by_id_xml(request, id):
    data = Product.objects.filter(pk=id)
    return HttpResponse(serializers.serialize('xml', data), content_type='application/xml')

def show_product_by_id_json(request, id):
    data = Product.objects.filter(pk=id)
    return HttpResponse(serializers.serialize('json', data), content_type='application/json')

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
    return render(request, 'register_ajax.html', {'form': form})


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
    return render(request, 'login_ajax.html', {'form': form})


def logout_user(request: Request) -> HttpResponse:
    logout(request)
    response = redirect('main:login')
    response.delete_cookie('last_login')
    return response

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_http_methods
import json

def get_products_json(request):
    source = request.GET.get('source', 'main')
    
    if source == 'my_products' and request.user.is_authenticated:
        products = Product.objects.filter(user=request.user)
    elif request.path == '/json/':
        products = Product.objects.filter(is_blacklisted=False)
    else:
        products = Product.objects.filter(is_blacklisted=False)
    
    data = []
    for product in products:
        data.append({
            'id': product.id,
            'name': product.name,
            'price': str(product.price),
            'discounted_price': str(product.discounted_price) if product.discounted_price else None,
            'description': product.description,
            'category': product.category,
            'thumbnail': product.thumbnail,
            'is_featured': product.is_featured,
            'is_official_store': product.is_official_store,
            'is_blacklisted': product.is_blacklisted,
            'user': product.user.username if product.user else 'Unknown',
            'created_at': product.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        })
    
    return JsonResponse(data, safe=False)

def get_product_detail_json(request, id):
    try:
        product = Product.objects.get(pk=id)
        
        if product.is_blacklisted and (not request.user.is_authenticated or product.user != request.user):
            return JsonResponse({'error': 'Product not found'}, status=404)
        
        data = {
            'id': product.id,
            'name': product.name,
            'price': str(product.price),
            'discounted_price': str(product.discounted_price) if product.discounted_price else None,
            'description': product.description,
            'category': product.category,
            'thumbnail': product.thumbnail,
            'is_featured': product.is_featured,
            'is_official_store': product.is_official_store,
            'is_blacklisted': product.is_blacklisted,
            'user': product.user.username if product.user else 'Unknown',
            'created_at': product.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        }
        
        return JsonResponse(data)
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)

@login_required(login_url='main:login')
@require_POST
def create_product_ajax(request):
    try:
        data = json.loads(request.body)
        
        product = Product.objects.create(
            user=request.user,
            name=data.get('name'),
            price=data.get('price'),
            discounted_price=data.get('discounted_price') or None,
            description=data.get('description'),
            category=data.get('category'),
            thumbnail=data.get('thumbnail'),
            is_featured=data.get('is_featured', False),
            is_official_store=data.get('is_official_store', False),
            is_blacklisted=data.get('is_blacklisted', False),
            brand_id=data.get('brand_id'),
            category_id=data.get('category_id'),
            shop_id=data.get('shop_id'),
            seo_keywords_ids=data.get('seo_keywords_ids'),
        )
        
        return JsonResponse({
            'status': 'success',
            'message': 'Product created successfully!',
            'product': {
                'id': product.id,
                'name': product.name,
                'price': str(product.price),
            }
        }, status=201)
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

@login_required(login_url='main:login')
@require_POST
def update_product_ajax(request, id):
    try:
        product = get_object_or_404(Product, pk=id, user=request.user)
        data = json.loads(request.body)
        
        product.name = data.get('name', product.name)
        product.price = data.get('price', product.price)
        product.discounted_price = data.get('discounted_price') or None
        product.description = data.get('description', product.description)
        product.category = data.get('category', product.category)
        product.thumbnail = data.get('thumbnail', product.thumbnail)
        product.is_featured = data.get('is_featured', product.is_featured)
        product.is_official_store = data.get('is_official_store', product.is_official_store)
        product.is_blacklisted = data.get('is_blacklisted', product.is_blacklisted)
        product.brand_id = data.get('brand_id', product.brand_id)
        product.category_id = data.get('category_id', product.category_id)
        product.shop_id = data.get('shop_id', product.shop_id)
        product.seo_keywords_ids = data.get('seo_keywords_ids', product.seo_keywords_ids)
        
        product.save()
        
        return JsonResponse({
            'status': 'success',
            'message': 'Product updated successfully!'
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

@login_required(login_url='main:login')
@require_POST
def delete_product_ajax(request, id):
    try:
        product = get_object_or_404(Product, pk=id, user=request.user)
        product_name = product.name
        product.delete()
        
        return JsonResponse({
            'status': 'success',
            'message': f'Product "{product_name}" deleted successfully!'
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

@require_POST
def login_ajax(request):
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return JsonResponse({
                'status': 'success',
                'message': f'Welcome back, {username}!',
                'username': username
            })
        else:
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid username or password'
            }, status=401)
            
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

@require_POST
def register_ajax(request):
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password1 = data.get('password1')
        password2 = data.get('password2')
        
        if password1 != password2:
            return JsonResponse({
                'status': 'error',
                'message': 'Passwords do not match'
            }, status=400)
        
        if len(password1) < 8:
            return JsonResponse({
                'status': 'error',
                'message': 'Password must be at least 8 characters long'
            }, status=400)
        
        from django.contrib.auth.models import User
        
        if User.objects.filter(username=username).exists():
            return JsonResponse({
                'status': 'error',
                'message': 'Username already exists'
            }, status=400)
        
        user = User.objects.create_user(username=username, password=password1)
        user.save()
        
        return JsonResponse({
            'status': 'success',
            'message': 'Account created successfully! Please log in.',
            'username': username
        }, status=201)
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

@require_POST
def logout_ajax(request):
    logout(request)
    return JsonResponse({
        'status': 'success',
        'message': 'Logged out successfully!'
    })