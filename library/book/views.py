from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.http import Http404
from django.db.models import Q

from authentication.decorators import role_required
from .models import Book
from author.models import Author



@role_required(0, 1)
def book_list(request):
    name = request.GET.get("name", "").strip()
    author = request.GET.get("author", "").strip()

    books = Book.get_all()

    if name:
        books = books.filter(name__icontains=name)

    if author:
        books = books.filter(
            Q(authors__name__icontains=author) |
            Q(authors__surname__icontains=author) |
            Q(authors__patronymic__icontains=author)
        )

    authors = Author.objects.all().order_by("surname", "name")

    return render(request, "book/book_list.html", {
        "books": books.distinct().order_by("id"),
        "authors": authors,
        "name": name,
        "author_id": author,
    })

@role_required(0, 1)
def book_detail(request, pk):
    book = Book.get_by_id(pk)

    if book is None:
        raise Http404

    return render(request, "book/book_detail.html", {
        "book": book,
    })

@role_required(1)
@require_http_methods(["GET", "POST"])
def book_admin_create(request):
    authors = Author.objects.all().order_by("surname", "name")

    name = ""
    description = ""
    count = "10"
    author_ids = []
    error = None

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        description = request.POST.get("description", "").strip()
        count = request.POST.get("count", "").strip()
        author_ids = request.POST.getlist("author_ids")

        error = Book.validate_book_data(name, description, count)

        if not error:
            selected_authors = Author.objects.filter(id__in=author_ids)
            book = Book.create(name, description, count, list(selected_authors))

            if book:
                return redirect("book_list")
            else:
                error = "Failed to create book. Please try again."

    context = {
        "authors": authors,
        "error": error,
        "name": name,
        "description": description,
        "count": count,
        "selected_author_ids": author_ids,
    }

    return render(request, "book/book_admin_create.html", context)

@role_required(1)
@require_http_methods(["GET", "POST"])
def book_admin_update(request, pk):
    book = Book.get_by_id(pk)
    if book is None:
        raise Http404("Book not found")

    authors = Author.objects.all().order_by("surname", "name")

    name = book.name
    description = book.description
    count = str(book.count)
    author_ids = [str(author.id) for author in book.authors.all()]
    error = None

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        description = request.POST.get("description", "").strip()
        count = request.POST.get("count", "").strip()
        author_ids = request.POST.getlist("author_ids")

        error = Book.validate_book_data(name, description, count)

        if not error:
            selected_authors = Author.objects.filter(id__in=author_ids)

            book.update(
                name=name,
                description=description,
                count=count
            )

            book.authors.clear()
            if selected_authors:
                book.add_authors(selected_authors)

            return redirect("book_list")

    return render(request, "book/book_admin_update.html", {
        "book": book,
        "authors": authors,
        "error": error,
        "name": name,
        "description": description,
        "count": count,
        "selected_author_ids": author_ids,
    })

@role_required(1)
@require_http_methods(["POST"])
def book_admin_delete(request, pk):
    Book.delete_by_id(pk)
    return redirect("book_list")