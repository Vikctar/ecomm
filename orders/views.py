from decimal import Decimal

from django.db import transaction
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from orders.models import Order, OrderItem
from orders.serializers import OrderSerializer, CreateOrderSerializer
from products.models import Product


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if hasattr(self.request.user, 'customer'):
            return Order.objects.filter(customer=self.request.user.customer)
        return Order.objects.none()

    @action(detail=False, methods=['post'])
    def create_order(self, request):
        """Create a new order with items"""
        serializer = CreateOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if not hasattr(request.user, 'customer'):
            return Response(
                {'error': 'Customer profile required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():
            # Calculate total and create order
            total_amount = Decimal('0.00')
            order_items_data = []

            for item_data in serializer.validated_data['items']:
                try:
                    product = Product.objects.get(id=item_data['product_id'])
                    quantity = int(item_data['quantity'])

                    if quantity > product.stock_quantity:
                        return Response(
                            {'error': f'Insufficient stock for {product.name}'},
                            status=status.HTTP_400_BAD_REQUEST
                        )

                    subtotal = product.price * quantity
                    total_amount += subtotal

                    order_items_data.append({
                        'product': product,
                        'quantity': quantity,
                        'price': product.price
                    })

                except (Product.DoesNotExist, ValueError, KeyError):
                    return Response(
                        {'error': 'Invalid product or quantity'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            # Create order
            order = Order.objects.create(
                customer=request.user.customer,
                total_amount=total_amount
            )

            # Create order items and update stock
            for item_data in order_items_data:
                OrderItem.objects.create(
                    order=order,
                    **item_data
                )

                # Update product stock
                item_data['product'].stock_quantity -= item_data['quantity']
                item_data['product'].save()

            return Response(
                OrderSerializer(order).data,
                status=status.HTTP_201_CREATED
            )
