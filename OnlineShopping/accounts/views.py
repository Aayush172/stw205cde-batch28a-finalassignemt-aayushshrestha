from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from .forms import LoginForm, ProfileForm
from accounts.auth import unauthenticated_user, admin_only, user_only
from django.contrib.auth.decorators import login_required

def homepage(request):
    return render(request, 'accounts/homepage.html')

@login_required
def logout_user(request):
    logout(request)
    return redirect('/login')


@unauthenticated_user
def login_user(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username=data['username'],
                                password=data['password'])
            if user is not None:
                if user.is_staff:
                    login(request, user)
                    return redirect('/admins/dashboard')
                elif not user.is_staff:
                    login(request, user)
                    return redirect('/')
            else:
                messages.add_message(request, messages.ERROR, 'Invalid username or password')
                return render(request, 'accounts/login.html', {'form_login': form})

    context={
        'form_login': LoginForm,
        'activate_login': 'active'


    }
    return render(request, 'accounts/login.html', context)


@unauthenticated_user
def register_user(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS,'User register successfully')
            return redirect('/login')
        else:
            messages.add_message(request, messages.ERROR,'Something went wrong')
            return render(request, 'accounts/register.html',{'form_register': form})

    context = {
        'form_register': UserCreationForm,
        'activate_register': 'active'

    }
    return render(request, 'accounts/register.html', context)



@login_required
@admin_only
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.add_message(request,messages.SUCCESS, 'Password Change Successfully')
            return redirect('/admins/dashboard')
        else:
            messages.add_message(request, messages.ERROR, 'Please verify the form field')
            return render(request, 'accounts/password_change.html',{'password_change_form':form})

    context = {
        'password_change_form': PasswordChangeForm(request.user)
    }
    return render(request, 'accounts/password_change.html', context)


@login_required
@user_only
def profile(request):
    profile = request.user.profile
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "Profile update successfully")
            return redirect('/profile')
    context = {
        'form': ProfileForm(instance=profile),
        'activate_profile': 'active'
    }
    return render(request, 'accounts/profile.html', context)
