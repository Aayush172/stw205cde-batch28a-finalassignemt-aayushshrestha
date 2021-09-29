from django.shortcuts import render, redirect
from .forms import CategoryForm, ProductForm, OrderForm
from django.contrib import messages
from .models import Category, Product, Cart, Order
from accounts.auth import admin_only, user_only
from django.contrib.auth.decorators import login_required
import os


def homepage(request):
    return render(request, 'products/homepage.html')


def about(request):
    context = {
        'activate_about': 'active'
    }
    return render(request, 'products/about.html', context)

@login_required
@admin_only
def category_form(request):
    if request.method == "POST":
        form = CategoryForm(request.POST, request.FILES)
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


def library(request):
    categories = Category.objects.all().order_by('-id')
    context = {
        'categories': categories,
        'activate_library': 'active'
    }
    return render(request, 'products/library.html', context)

@login_required
@user_only
def add_to_cart(request, product_id):
    user = request.user
    product = Product.objects.get(id=product_id)

    check_item_presence = Cart.objects.filter(user=user, product=product)
    if check_item_presence:
        messages.add_message(request, messages.ERROR, 'Item is already present in cart')
        return redirect('/products/get_product_user')
    else:
        cart = Cart.objects.create(product=product, user=user)
        if cart:
            messages.add_message(request, messages.SUCCESS, 'Item added to cart')
            return redirect('/products/mycart')
        else:
            messages.add_message(request, messages.ERROR, 'Unable to add item to cart')

@login_required
@user_only
def show_cart_items(request):
    user = request.user
    items = Cart.objects.filter(user=user)
    context = {
        'items': items,
        'activate_my_cart': 'active'
    }
    return render(request, 'products/mycart.html', context)


@login_required
@user_only
def remove_cart_item(request, cart_id):
    item = Cart.objects.get(id=cart_id)
    item.delete()
    messages.add_message(request, messages.SUCCESS, 'Cart item removed successfully')
    return redirect('/products/mycart')

@login_required
@user_only
def order_form(request, product_id, cart_id):
    user = request.user
    product = Product.objects.get(id=product_id)
    cart_item = Cart.objects.get(id=cart_id)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            quantity = request.POST.get('quantity')
            price = product.product_price
            total_price = int(quantity)*int(price)
            contact_no = request.POST.get('contact_no')
            contact_address = request.POST.get('contact_address')
            payment_method = request.POST.get('payment_method')
            order = Order.objects.create(product=product,
                                         user =user,
                                         quantity=quantity,
                                         total_price=total_price,
                                         contact_no = contact_no,
                                         contact_address =contact_address,
                                         status="Pending",
                                         payment_method= payment_method,
                                         payment_status=False
            )
            if order:
                messages.add_message(request, messages.SUCCESS, 'Item Ordered. Continue Payment for Verification')
                cart_item.delete()
                return redirect('/products/my_order')
                # context = {
                #     'order': order,
                #     'cart': cart_item
                # }
                # return render(request, 'products/esewa_payment.html', context)
        else:
            messages.add_message(request, messages.ERROR, 'Something went wrong')
            return render(request, 'products/order_form.html', {'order_form':form})
    context = {
        'order_form': OrderForm
    }
    return render(request, 'products/order_form.html', context)


@login_required
@user_only
def my_order(request):
    user = request.user
    items = Order.objects.filter(user=user).order_by('-id')
    context = {
        'items':items,
        'activate_myorders':'active'
    }
    return render(request, 'products/my_order.html', context)