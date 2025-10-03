from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from .models import Book


class BookApiTests(APITestCase):
    def setUp(self):
        Book.objects.create(title="Clean Code", author="Robert C. Martin")
        Book.objects.create(title="Two Scoops of Django", author="Daniel Roy Greenfeld")

    def test_public_can_list_books_via_books_all(self):
        url = reverse('book_all-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.json()), 2)

    def test_public_can_list_books_via_books(self):
        url = reverse('book-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.json()), 2)

    def test_create_requires_authentication(self):
        url = reverse('book_all-list')
        payload = {"title": "Django for APIs", "author": "William S. Vincent"}
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_can_create_book(self):
        user = User.objects.create_user(username='tester', password='pass1234')
        token, _ = Token.objects.get_or_create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

        url = reverse('book_all-list')
        payload = {"title": "Django Unleashed", "author": "Andrew Pinkham"}
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Book.objects.filter(title="Django Unleashed").exists())