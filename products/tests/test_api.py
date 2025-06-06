from datetime import datetime, timedelta
from decimal import Decimal

from django.contrib.auth.models import User
from django.urls import reverse
from oauth2_provider.models import Application, AccessToken
from rest_framework import status
from rest_framework.test import APITestCase

from products.models import Category, Product


class ProductAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

        self.application = Application.objects.create(
            name="Test Application",
            user=self.user,
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.GRANT_AUTHORIZATION_CODE,
        )

        self.access_token = AccessToken.objects.create(
            user=self.user,
            scope='read write',
            expires=datetime.utcnow() + timedelta(seconds=300),
            token='secret-access-token-key',
            application=self.application
        )

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token.token)

        self.category = Category.objects.create(name="Electronics", slug="electronics")
        self.product = Product.objects.create(
            name="Smartphone",
            slug="smartphone",
            description="Latest smartphone",
            price=Decimal('599.99'),
            stock_quantity=10
        )
        self.product.categories.add(self.category)

    def test_list_products(self):
        url = reverse('product-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_create_product(self):
        url = reverse('product-list')
        data = {
            'name': 'Laptop',
            'slug': 'laptop',
            'description': 'Gaming laptop',
            'price': '1299.99',
            'stock_quantity': 5,
            'category_ids': [self.category.id]
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
