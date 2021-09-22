from django.shortcuts import render, redirect
from .forms import CategoryForm, ProductForm
from django.contrib import messages
from .models import Category, Product
from accounts.auth import admin_only, user_only
from django.contrib.auth.decorators import login_required
import os

def homepage(request):
    return render(request, 'products/homepage.html')

@login_required
@admin_only
def category_form(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request,messages.SUCCESS, "Category Added Successfully")
            return redirect("/products/get_category")
        else:
            messages.add_message(request, messages.ERROR, 'Unable to add')
            return render(request, 'products/category_form.html', {'form_category': form})

    context = {
        'form_category': CategoryForm,
        'activate_category': 'active'
    }
    return render(request, 'products/category_form.html', context)

@login_required
@admin_only
def get_category(request):
    categories = Category.objects.all().order_by('-id')
    context = {
        'categories': categories,
        'activate_category': 'active'
    }
    return render(request, 'products/get_category.html', context)

@login_required
@admin_only
def delete_category(request, category_id):
    category = Category.objects.get(id=category_id)
    category.delete()
    messages.add_message(request, messages.SUCCESS, 'Category Deleted Successfully')
    return redirect('/products/get_category')

@login_required
@admin_only
def category_update_form(request, category_id):
    category = Category.objects.get(id=category_id)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.add_message(request,messages.SUCCESS, 'Category Updated Successfully')
            return redirect("/products/get_category")
        else:
            messages.add_message(request, messages.ERROR, 'Unable to updated')
            return render(request, 'products/category_update_form.html', {'form_category': form})

    context = {
        'form_category': CategoryForm(instance=category),
        'activate_category': 'active'
    }
    return render(request, 'products/category_update_form.html', context)

@login_required
@admin_only
def product_form(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(request,messages.SUCCESS, "Product Added Successfully")
            return redirect("/products/get_product")
        else:
            messages.add_message(request, messages.ERROR, 'Unable to add')
            return render(request, 'products/product_form.html', {'form_product': form})

    context = {
        'form_product': ProductForm,
        'activate_product': 'active'
    }
    return render(request, 'products/product_form.html', context)

@login_required
@admin_only
def get_product(request):
    products = Product.objects.all().order_by('-id')
    context = {
        'products': products,
        'activate_product': 'active'
    }
    return render(request, 'products/get_product.html', context)

@login_required
@admin_only
def delete_product(request, product_id):
    product = Product.objects.get(id=product_id)
    os.remove(product.product_image.path)
    product.delete()
    messages.add_message(request, messages.SUCCESS, 'Product Deleted Successfully')
    return redirect('/products/get_product')


@login_required
@admin_only
def product_update_form(request, product_id):
    product = Product.objects.get(id=product_id)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.add_message(request,messages.SUCCESS, 'Product Updated Successfully')
            return redirect("/products/get_product")
        else:
            messages.add_message(request, messages.ERROR, 'Unable to updated')
            return render(request, 'products/product_form.html', {'form_product': form})

    context = {
        'form_product': ProductForm(instance=product),
        'activate_product': 'active'
    }
    return render(request, 'products/product_update_form.html', context)


def show_categories(request):
    categories = Category.objects.all().order_by('-id')
    context = {
        'categories': categories,
        'activate_category_user': 'active'
    }
    return render(request, 'products/show_categories.html', context)


def show_products(request):
    products = Product.objects.all().order_by('-id')
    context = {
        'products': products,
        'activate_product_user': 'active'
    }
    return render(request, 'products/show_products.html', context)
