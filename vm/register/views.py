from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from vm.register_user.forms import RegisterForm

from django.contrib.auth import login, authenticate, logout
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.forms import PasswordResetForm



def register_user(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully!")
            return redirect("login")  # Redirect to a login page or any other page
    else:
        form = RegisterForm()

    return render(request, "templates/register.html", {"form": form})
@csrf_protect
def login_user(request):
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                if user.is_staff:
                    admin_url = reverse('admin:index')
                    return redirect(admin_url)
                else:
                    # Get the current user
                    current_user = request.user

            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, "register/login.html", {"login_user": form, "facebook_app_id": "your-facebook-app-id"})


def logout_user(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("home")


def password_reset(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Password reset email sent.')
            return redirect('login')  # replace 'login' with the name of your login view
        else:
            messages.error(request, 'Invalid email.')
    else:
        form = PasswordResetForm()
    return render(request, 'password_reset.html', {'form': form})


def password_reset_confirm(request):
    password_reset_confirm(request)
    messages.info(request, "Your password has been reset. You may now log in with your new password.")
    return redirect("login")


