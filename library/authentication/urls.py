from django.urls import path
from .views import (
    register_view,
    login_view,
    logout_view,
    user_admin_list,
    user_admin_detail,
    user_books
)


urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path("users/", user_admin_list, name="user_admin_list"),
    path("users/<int:pk>/", user_admin_detail, name="user_admin_detail"),
    path("users/<int:pk>/books/", user_books, name="user_books"),
]