from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import admin

# Create your views here.
def index(request):
    return render(request, 'portfolio_app/index.html')