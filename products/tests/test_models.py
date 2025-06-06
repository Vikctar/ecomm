from django.test import TestCase

from products.models import Category


class CategoryModelTest(TestCase):
    def setUp(self):
        self.root_category = Category.objects.create(name="All Products", slug="all-products")
        self.bakery = Category.objects.create(name="Bakery", slug="bakery", parent=self.root_category)
        self.bread = Category.objects.create(name="Bread", slug="bread", parent=self.bakery)

    def test_category_hierarchy(self):
        self.assertEqual(self.bread.parent, self.bakery)
        self.assertEqual(self.bakery.parent, self.root_category)
        self.assertIn(self.bakery, self.root_category.children.all())

    def test_get_ancestors(self):
        ancestors = self.bread.get_parents()
        self.assertEqual(len(ancestors), 2)
        self.assertEqual(ancestors[0], self.root_category)
        self.assertEqual(ancestors[1], self.bakery)

    def test_full_path(self):
        expected_path = "All Products > Bakery > Bread"
        self.assertEqual(self.bread.get_full_path(), expected_path)
