from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpRequest as Request

# Create your views here.
def show_main(request: Request) -> HttpResponse:
    # directly render the main.html template without any context
    return render(request,'main.html')