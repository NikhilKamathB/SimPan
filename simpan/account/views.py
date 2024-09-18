from django.urls import reverse
from django.contrib import messages
from django.utils.http import urlencode
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login


def login_view(request):
    next_url = request.GET.get("next") or reverse("home:home")
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        next_url = request.POST.get("next") or reverse("home:home")
        user = authenticate(username=email, password=password)
        if user is None:
            if User.objects.filter(username=email).exists():
                messages.error(request, "You are an active user. Invalid email or password. Login with correct credentials.")
                login_url = reverse("account:login")
                return redirect(f"{login_url}?{urlencode({'next': next_url})}")
            user = User.objects.create_user(username=email, email=email, password=password)
        login(request, user)
        messages.success(request, "Login successful. Welcome to SimPan.")
        return redirect(next_url)
    return render(request, 'account/login.html', {'next_url': next_url})
