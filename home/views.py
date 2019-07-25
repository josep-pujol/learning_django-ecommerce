from django.shortcuts import render


def index(request):
    """Render index page"""
    return render(request, 'index.html')
