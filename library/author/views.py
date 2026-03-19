from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.http import Http404
from django.contrib import messages
from authentication.decorators import role_required
from .models import Author


@role_required(1)
def author_admin_list(request):
    authors = Author.get_all().order_by("id")
    return render(request, "author/author_admin_list.html",
                  {"authors": authors})

@role_required(1)
@require_http_methods(["GET", "POST"])
def author_admin_create(request):
    context = {}

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        surname = request.POST.get("surname", "").strip()
        patronymic = request.POST.get("patronymic", "").strip()

        context = {
            "name": name,
            "surname": surname,
            "patronymic": patronymic,
        }

        error = Author.validate_author_data(name, surname, patronymic)

        if error:
            context["error"] = error
        else:
            author = Author.create(name, surname, patronymic)

            if author is None:
                context["error"] = "Author already exists."
            else:
                return redirect("author_admin_list")

    return render(request, "author/author_admin_create.html", context)

@role_required(1)
@require_http_methods(["GET", "POST"])
def author_admin_update(request, pk):
    author = Author.get_by_id(pk)

    if author is None:
        raise Http404

    context = {
        "author": author,
        "name": author.name,
        "surname": author.surname,
        "patronymic": author.patronymic,
    }

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        surname = request.POST.get("surname", "").strip()
        patronymic = request.POST.get("patronymic", "").strip()

        context["name"] = name
        context["surname"] = surname
        context["patronymic"] = patronymic

        error = Author.validate_author_data(name, surname, patronymic)

        if error:
            context["error"] = error
        else:
            existing_author = Author.objects.filter(
                name=name,
                surname=surname,
                patronymic=patronymic
            ).exclude(id=author.id).exists()

            if existing_author:
                context["error"] = "Author with these details already exists."
            else:
                author.update(
                    name=name,
                    surname=surname,
                    patronymic=patronymic
                )
                return redirect("author_admin_list")

    return render(request, "author/author_admin_update.html", context)

@role_required(1)
@require_http_methods(["POST"])
def author_admin_delete(request, pk):
    if not Author.delete_by_id(pk):
        messages.error(request, "Cannot delete author, author added to book.")

    return redirect("author_admin_list")

