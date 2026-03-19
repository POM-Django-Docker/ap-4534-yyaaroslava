from django.urls import path
from .views import (
    author_admin_list,
    author_admin_create,
    author_admin_update,
    author_admin_delete,
)


urlpatterns = [
    path('admin/', author_admin_list, name="author_admin_list"),
    path("admin/create/", author_admin_create, name="author_admin_create"),
    path("admin/update/<int:pk>/", author_admin_update, name="author_admin_update"),
    path("admin/delete/<int:pk>/", author_admin_delete, name="author_admin_delete"),
]