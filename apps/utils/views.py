from django.shortcuts import render


def dashboard(request):
    page_title = 'Dashboard'

    context = {
        'page_title': page_title
    }
    return render(request, 'dashboard/dashboard.html', context)


def login(request):
    return render(request, 'login/login.html')

