from rest_framework import serializers

from products.models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    full_path = serializers.ReadOnlyField(source='get_full_path')

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'parent', 'description', 'children', 'full_path', 'created_at']

    def get_children(self, obj):
        if obj.children.exists():
            return CategorySerializer(obj.children.all(), many=True).data
        return []


class ProductSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    category_ids = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        many=True,
        write_only=True,
        source='categories'
    )

    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'description', 'price', 'stock_quantity',
                  'categories', 'category_ids', 'is_active', 'is_in_stock', 'created_at']
