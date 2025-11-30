from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import User

@login_required
def delete_user(request):
    user = request.user
    # Logout the user first
    logout(request)
    # Delete the user account
    user.delete()
    return redirect('home')  # Redirect to home or goodbye page
