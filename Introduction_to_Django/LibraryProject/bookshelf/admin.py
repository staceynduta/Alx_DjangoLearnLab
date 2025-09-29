from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Product, Book

# Basic registration
admin.site.register(Book)

# Or with customization:
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'publication_year']
    list_filter = ['publication_year', 'author']
    search_fields = ['title', 'author']
    ordering = ['title']
    list_per_page = 25

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'in_stock', 'created_at']
    list_filter = ['category', 'in_stock', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['price', 'in_stock']
    ordering = ['name']
    list_per_page = 25

# Customize admin site
admin.site.site_header = "Book Store Management System"
admin.site.site_title = "Book Store Admin"
admin.site.index_title = "Welcome to Book Store Management"

# ============================================
# STEP 3: Test Book model in Django shell
# ============================================
# python manage.py shell

from book_store.models import Book

# Create books
book1 = Book.objects.create(
    title="The Great Gatsby",
    author="F. Scott Fitzgerald",
    publication_year=1925
)

book2 = Book.objects.create(
    title="To Kill a Mockingbird",
    author="Harper Lee",
    publication_year=1960
)

book3 = Book.objects.create(
    title="1984",
    author="George Orwell",
    publication_year=1949
)

# Retrieve all books
all_books = Book.objects.all()
for book in all_books:
    print(book)

# Filter books by author
orwell_books = Book.objects.filter(author="George Orwell")

# Filter books by publication year range
classic_books = Book.objects.filter(
    publication_year__gte=1900,
    publication_year__lte=1950
)

# Order books by publication year
books_by_year = Book.objects.all().order_by('publication_year')
books_by_year_desc = Book.objects.all().order_by('-publication_year')

# Search for books with title containing specific text
gatsby_books = Book.objects.filter(title__icontains="gatsby")

# Update a book
book = Book.objects.get(id=1)
book.publication_year = 1926
book.save()

# Delete a book
book = Book.objects.get(id=1)
book.delete()

# Bulk create
books = [
    Book(title="Pride and Prejudice", author="Jane Austen", publication_year=1813),
    Book(title="The Catcher in the Rye", author="J.D. Salinger", publication_year=1951),
    Book(title="Harry Potter", author="J.K. Rowling", publication_year=1997),
]
Book.objects.bulk_create(books)

# Count books
total_books = Book.objects.count()

# Get books by specific author
author_name = "George Orwell"
author_books = Book.objects.filter(author=author_name)

# Get the latest book
latest_book = Book.objects.latest('publication_year')

# Get the oldest book
oldest_book = Book.objects.earliest('publication_year')

# Check if a book exists
exists = Book.objects.filter(title="1984").exists()

# ============================================
# STEP 4: Add Book views (Optional)
# ============================================