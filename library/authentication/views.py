from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import Http404
from .decorators import role_required
from .models import CustomUser
from order.models import Order

def register_view(request):
    if request.method == 'POST':
        user = CustomUser.objects.create_user(
            email=request.POST.get('email'),
            password=request.POST.get('password'),
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            middle_name=request.POST.get('middle_name', ''),
            role=int(request.POST.get('role', 0)), 
            is_active=True 
        )
        
        if user:
            return redirect('login')
            
    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_exists = CustomUser.get_by_email(email)
        
        if user_exists:
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')

        return render(request, 'login.html', {'error': 'Invalid email or password'})
            
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('home')


@role_required(1)
def user_admin_list(request):
    users = CustomUser.get_all().order_by("id")
    return render(request, "user_admin_list.html", {"users": users})


@role_required(1)
def user_admin_detail(request, pk):
    user_obj = CustomUser.get_by_id(pk)
    if user_obj is None:
        raise Http404
    return render(request, "user_admin_detail.html", {"user_obj": user_obj})

@role_required(1)
def user_books(request, pk):
    user_obj = CustomUser.get_by_id(pk)

    if user_obj is None:
        raise Http404

    orders = Order.objects.filter(user=user_obj, end_at__isnull=True)

    return render(request, "user_books.html", {
        "user_obj": user_obj,
        "orders": orders,
    })
