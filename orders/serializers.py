from rest_framework import serializers

from orders.models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')
    subtotal = serializers.ReadOnlyField()

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'quantity', 'price', 'subtotal']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    customer_email = serializers.ReadOnlyField(source='customer.user.email')

    class Meta:
        model = Order
        fields = ['id', 'customer', 'customer_email', 'status', 'total_amount', 'items', 'created_at', 'updated_at']


class CreateOrderSerializer(serializers.Serializer):
    items = serializers.ListField(
        child=serializers.DictField(
            child=serializers.CharField()
        )
    )
    shipping_address = serializers.CharField()
    notes = serializers.CharField(required=False, allow_blank=True)
