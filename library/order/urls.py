from django.urls import path
from . import views

urlpatterns = [
    path('all/', views.all_orders_view, name='all_orders'),
    path('my/', views.my_orders_view, name='my_orders'),
    path('create/<int:book_id>/', views.order_create_view, name='order_create'),
    path('close/<int:order_id>/', views.order_close_view, name='order_close'),
]