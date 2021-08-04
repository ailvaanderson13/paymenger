from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from apps.agiota import models


def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('utils:login')

    page_title = 'Dashboard'

    context = {
        'page_title': page_title
    }
    return render(request, 'dashboard/dashboard.html', context)


def acesso(request):
    if request.user.is_authenticated:
        return redirect('utils:dashboard')

    erro = False
    msg = None
    pagamento = True
    notification = None

    if request.method == 'POST':
        email = request.POST.get('email', None)
        senha = request.POST.get('senha', None)

        if email:
            pagamento = models.Agiota.objects.filter(email=email)
            if pagamento:
                pagamento = pagamento.last()
                if pagamento.pagou:
                    user = authenticate(username=email, password=senha)

                    if user:
                        login(request, user)
                        return redirect('utils:dashboard')
                    else:
                        notification = 'danger'
                        msg = 'Usuário ou senha inválidos!'
                else:
                    notification = 'danger'
                    msg = 'Pagamento não identificado! Entre em contato com o suporte!'
    context = {
        'erro': erro, 'msg': msg, 'notification': notification
    }
    return render(request, 'login/login.html', context)
