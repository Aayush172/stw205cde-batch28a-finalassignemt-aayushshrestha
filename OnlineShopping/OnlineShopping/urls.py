from django.urls import path, include

urlpatterns = [
    path('products/', include('products.urls')),
    path('admins/', include('admins.urls')),
    path('', include('accounts.urls')),

]
