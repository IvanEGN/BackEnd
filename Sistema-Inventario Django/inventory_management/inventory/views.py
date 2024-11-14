from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import generics
from .models import Product, Supplier, Order
from .forms import CustomUserCreationForm, ProductForm, SupplierForm, OrderForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth import logout
from .serializers import ProductSerializer, SupplierSerializer, OrderSerializer

# Create your views here.
# view home
def home(request):
    context = {
        'show_buttons': ['inicio', 'acerca_de', 'iniciar_sesion', 'registrarse']
    }
    return render(request, 'home.html', context)

# view about us
def about(request):
    return render(request, 'about.html')

# view login
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('inventario')  # Asegúrate de que 'home' es el nombre de la URL a la que quieres redirigir después del login.
            else:
                form.add_error(None, "Nombre de usuario o contraseña incorrectos")
        # Si el formulario no es válido, renderiza la página de login con el formulario que contiene los errores.
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# view register
def register_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Inicia sesión al usuario y redirige a la página de inicio
            user_login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

# view inventory
def inventory_user(request):
    products = Product.objects.all()
    suppliers = Supplier.objects.all()
    orders = Order.objects.filter(status='pending')  # O modificar según lo que necesites mostrar

    context = {
        'products': products,
        'suppliers': suppliers,
        'orders': orders,
    }

    return render(request, 'inventario.html', context)

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventario')
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})

@login_required
def add_supplier(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventario')
    else:
        form = SupplierForm()
    return render(request, 'add_supplier.html', {'form': form})

@login_required
def add_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventario')
    else:
        form = OrderForm()
    return render(request, 'add_order.html', {'form': form})

@require_POST
def delete_product(request, id):
    product = get_object_or_404(Product, id=id)
    product.delete()
    return redirect('inventario')

@require_POST
def delete_supplier(request, id):
    supplier = get_object_or_404(Supplier, id=id)
    supplier.delete()
    return redirect('inventario')

@require_POST
def delete_order(request, id):
    order = get_object_or_404(Order, id=id)
    order.delete()
    return redirect('inventario')

def logout_view(request):
    logout(request)
    return redirect('login')  # Redireccionar al usuario a la página de inicio de sesión después del logout.

class ProductListCreate(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class SupplierListCreate(generics.ListCreateAPIView):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer

class OrderListCreate(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
