from django.db.models import Avg
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from products.models import Category, Product
from products.serializers import CategorySerializer, ProductSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'

    @action(detail=True, methods=['get'])
    def average_price(self, request, slug=None):
        """Get average product price for a category and its subcategories"""
        category = self.get_object()

        # Get all children categories
        child_categories = [category] + category.get_children()

        # Calculate average price for products in these categories
        avg_price = Product.objects.filter(
            categories__in=child_categories,
            is_active=True
        ).aggregate(avg_price=Avg('price'))['avg_price']

        return Response({
            'category': category.name,
            'full_path': category.get_full_path(),
            'average_price': avg_price or 0,
            'total_products': Product.objects.filter(
                categories__in=child_categories,
                is_active=True
            ).count()
        })


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        queryset = super().get_queryset()
        category_slug = self.request.query_params.get('category', None)

        if category_slug:
            try:
                category = Category.objects.get(slug=category_slug)
                child_categories = [category] + category.get_children()
                queryset = queryset.filter(categories__in=child_categories)
            except Category.DoesNotExist:
                pass

        return queryset.distinct()
