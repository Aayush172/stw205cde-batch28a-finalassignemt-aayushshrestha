from django.shortcuts import render, redirect
from .forms import CategoryForm, ProductForm
from django.contrib import messages
from .models import Category, Product


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


def get_category(request):
    categories = Category.objects.all().order_by('-id')
    context = {
        'categories': categories,
        'activate_category': 'active'
    }
    return render(request, 'products/get_category.html', context)