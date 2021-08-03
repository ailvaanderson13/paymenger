from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect


def dashboard(request):
    page_title = 'Dashboard'

    context = {
        'page_title': page_title
    }
    return render(request, 'dashboard/dashboard.html', context)


def acesso(request):
    erro = False
    msg = None

    if request.method == 'POST':
        email = request.POST.get('email', None)
        senha = request.POST.get('senha', None)

        user = authenticate(username=email, password=senha)

        if user:
            login(request, user)
            return redirect('utils:dashboard')
        else:
            erro = True
            msg = 'Usuário ou senha inválidos!'

    context = {
        'erro': erro, 'msg': msg
    }
    return render(request, 'login/login.html', context)
