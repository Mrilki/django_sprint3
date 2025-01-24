from django.shortcuts import render

# Create your views here.


def about(request):
    """Обрабатывает запрос по адресу pages/about/"""
    return render(request, 'pages/about.html')


def rules(request):
    """Обрабатывает запрос по адресу pages/rules/"""
    return render(request, 'pages/rules.html')
