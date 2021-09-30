from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.homepage),
    path('login', views.login_user),
    path('register', views.register_user),
    path('profile', views.profile),
    path('logout', views.logout_user),
    path('password_change', views.change_password),

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='accounts/mypassword_reset_form.html'),
         name='password_reset'),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='accounts/mypassword_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='accounts/mypassword_reset_confirm.html'),
         name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='accounts/mypassword_reset_complete.html'),
         name='password_reset_complete'),


]
