from django.urls import path
from .views import (
    book_list,
    book_detail,
    book_admin_create,
    book_admin_update,
    book_admin_delete,
)

urlpatterns = [
    path("", book_list, name="book_list"),
    path("<int:pk>/", book_detail, name="book_detail"),
    path("admin/create/", book_admin_create, name="book_admin_create"),
    path("admin/edit/<int:pk>/", book_admin_update, name="book_admin_update"),
    path("admin/delete/<int:pk>/", book_admin_delete, name="book_admin_delete"),
]