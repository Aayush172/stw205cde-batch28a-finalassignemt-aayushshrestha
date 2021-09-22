from django.shortcuts import redirect

# to check if the user is logged in or not
def unauthenticated_user(view_function):
    def wrapper_function(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/products/homepage')
        else:
            return view_function(request, *args, **kwargs)
    return wrapper_function

# check i f the user is admin
# and if the user is admin, it gives access to admin pages
# and if the user is not admin , it redirect to user dashboard

def admin_only(view_function):
    def wrapper_function(request, *args, **kwargs):
        if request.user.is_staff:
            return view_function(request, *args, **kwargs)

        else:
            return redirect('/products/homepage')

    return wrapper_function

# check if the user is normal user
# and if the user is normal user , it gives access to user pages
# and if the user is not normal user  , it redirect to admin dashboard
def user_only(view_function):
    def wrapper_function(request, *args, **kwargs):
        if request.user.is_staff:
            return redirect('/admins/dashboard')
        else:
            return view_function(request, *args, **kwargs)
    return wrapper_function


