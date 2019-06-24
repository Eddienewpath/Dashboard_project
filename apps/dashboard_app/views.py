from django.shortcuts import render, redirect 


def index(request):
    return render(request, 'dashboard_app/index.html')


def login(request):
    return render(request, 'dashboard_app/login.html')


def register(request):
    return render(request, 'dashboard_app/register.html')