from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Book

def book_list(request):
    author = request.GET.get('author', None)
    
    if author:
        books = Book.objects.filter(author=author).order_by('publication_year')
    else:
        books = Book.objects.all().order_by('title')
    
    return render(request, 'books/list.html', {'books': books})

def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'books/detail.html', {'book': book})

def books_by_author_json(request, author):
    books = Book.objects.filter(
        author__icontains=author
    ).order_by('publication_year').values('id', 'title', 'author', 'publication_year')
    
    return JsonResponse(list(books), safe=False)

def books_by_year_range(request):
    start_year = request.GET.get('start', 1900)
    end_year = request.GET.get('end', 2024)
    
    books = Book.objects.filter(
        publication_year__gte=start_year,
        publication_year__lte=end_year
    ).order_by('-publication_year')
    
    return render(request, 'books/year_range.html', {
        'books': books,
        'start_year': start_year,
        'end_year': end_year
    })

