from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse('home page')

def index(request):
    return render(request, 'portfolio_app/index.html')