from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from datetime import timedelta
from .models import Order
from book.models import Book
from authentication.decorators import role_required

@role_required(1)
def all_orders_view(request):
    orders = Order.get_all()
    return render(request, 'order/all_orders.html', {'orders': orders})

@role_required(0)
def my_orders_view(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'order/my_orders.html', {'orders': orders})

@role_required(0)

def order_create_view(request, book_id):
    if request.method == "POST": 
        book = Book.get_by_id(book_id)
        if not book:
            return redirect('book_list')

        if book.count > 0:
            plated_end = timezone.now() + timedelta(days=14)
            new_order = Order.create(user=request.user, book=book, plated_end_at=plated_end)
            if new_order:
                book.update(count=book.count - 1) 
    return redirect('my_orders') 

@role_required(1)
def order_close_view(request, order_id):
    order = Order.get_by_id(order_id)
    if order:
        if not order.end_at:
            order.update(end_at=timezone.now())
            order.book.count += 1
            order.book.save()
    return redirect('all_orders')