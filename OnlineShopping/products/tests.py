from django.test import SimpleTestCase, TestCase, Client
from django.urls import reverse, resolve
from products.views import about, homepage, category_form, delete_category
from .models import Category, Cart, Product

class TestUrls(SimpleTestCase):
    def test_homepage(self):
        url = reverse('homepage')
        self.assertEquals(resolve(url).func, homepage)

    def test_delete_category(self):
        url = reverse('delete_category', args=[1])
        self.assertEquals(resolve(url).func, delete_category)

    def test_category_form_url(self):
        url = reverse('category_form')
        self.assertEquals(resolve(url).func, category_form)

class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.about_url = reverse('about')
        self.show_library_url = reverse('library')
    def test_about(self):
        response = self.client.get(self.about_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/about.html')
    def test_library(self):
        response = self.client.get(self.show_library_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/library.html')

class TestModels(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            product_name='Smartphone',
            product_price="18000"
        )
        self.category = Category.objects.create(
            category_name='Top Seller',
            category_description="High Top Seller Products",
        )
    def test_food_menu_model(self):
        self.assertEquals(self.product.product_name, 'Smartphone')
    def test_food_category_model(self):
        self.assertEquals(self.category.category_name, 'Top Seller')
