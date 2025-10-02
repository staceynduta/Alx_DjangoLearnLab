from django.urls import path, include
from api.views import BookList  # Import BookList view

urlpatterns = [
    path('books/', BookList.as_view(), name='book-list'),  # Maps to the BookList view
    path('api/', include('api.urls')),  # Includes URLs from the api app
]