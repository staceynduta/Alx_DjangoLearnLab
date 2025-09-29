# Create your models here.
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
from datetime import datetime

# Category choices for Book model
CATEGORY_CHOICES = [
    ('fiction', 'Fiction'),
    ('nonfiction', 'Non-Fiction'),
    ('science', 'Science'),
    ('history', 'History'),
    ('biography', 'Biography'),
    ('other', 'Other'),
]

# ============================================
# Book Model
# ============================================

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()
    
    def __str__(self):
        return f"{self.name} by {self.author} ({self.publication_year})"
        return f"{self.name} by {self.author} ({self.publication_year})"
        return f"{self.title} by {self.author}"
    
    class Meta:
        ordering = ['title']
        verbose_name = 'Book'
        verbose_name_plural = 'Books'

# ============================================
# Enhanced Book Model (Optional - with validations)
# ============================================

class Book(models.Model):
    title = models.CharField(
        max_length=200,
        help_text="Enter the book title"
    )
    author = models.CharField(
        max_length=100,
        help_text="Enter the author's name"
    )
    publication_year = models.IntegerField(
        validators=[
            MinValueValidator(1000),
            MaxValueValidator(datetime.now().year)
        ],
        help_text="Enter the publication year"
    )
    
    def __str__(self):
        return f"{self.title} by {self.author} ({self.publication_year})"
    
    class Meta:
        ordering = ['title']
        verbose_name = 'Book'
        verbose_name_plural = 'Books'
        indexes = [
            models.Index(fields=['author']),
            models.Index(fields=['publication_year']),
        ]
    
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default='other'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    in_stock = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['category']),
            models.Index(fields=['price']),
        ]
    
    def __str__(self):
        return f"{self.name} by {self.author}"