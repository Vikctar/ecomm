import datetime
from datetime import timedelta
from decimal import Decimal

from django.contrib.auth.models import User
from django.urls import reverse
from oauth2_provider.models import Application, AccessToken
from rest_framework import status
from rest_framework.test import APITestCase

from customers.models import Customer
from orders.models import Order
from products.models import Product


class OrderAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='customer',
            email='customer@example.com',
            password='testpass123'
        )

        self.customer = Customer.objects.create(
            user=self.user,
            phone_number='+254700000000'
        )

        # Setup OAuth2
        self.application = Application.objects.create(
            name="Test Application",
            user=self.user,
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.GRANT_AUTHORIZATION_CODE,
        )

        self.access_token = AccessToken.objects.create(
            user=self.user,
            scope='read write',
            expires=datetime.datetime.now() + timedelta(seconds=300),
            token='customer-access-token',
            application=self.application
        )

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token.token)

        self.product = Product.objects.create(
            name="Test Product",
            slug="test-product",
            description="Test description",
            price=Decimal('99.99'),
            stock_quantity=10
        )

    def test_create_order(self):
        url = reverse('order-create-order')
        data = {
            'items': [
                {
                    'product_id': str(self.product.id),
                    'quantity': '2'
                }
            ],
            'shipping_address': '456 Delivery Street',
            'notes': 'Test order'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verify order was created
        order = Order.objects.get(id=response.data['id'])
        self.assertEqual(order.customer, self.customer)
        self.assertEqual(order.items.count(), 1)
        self.assertEqual(order.total_amount, Decimal('199.98'))
