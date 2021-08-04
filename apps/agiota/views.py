from django.shortcuts import render, redirect
from . import forms, models


def create_update_agiota(request, pk=None):
    if not request.user.is_authenticated:
        return redirect('utils:acesso')

    page_title = "Cadastro de Agiota" if not pk else "Editar Agiota"
    form = forms.AgiotaForm()
    agiota = None
    notification = None
    msg = None

    if pk:
        agiota = models.Agiota.objects.filter(pk=pk)
        agiota = agiota.last()
        if agiota:
            form = forms.AgiotaForm(instance=agiota)
        else:
            msg = "Nenhum agiota encontrado!"
            notification = "danger"

    if request.method == 'POST':
        if agiota:
            form = forms.AgiotaForm(request.POST, instance=agiota)
            msg = "Cadastro Atualizado com sucesso!"
            notification = "success"
        else:
            form = forms.AgiotaForm(request.POST)
            msg = "Agiota Cadastrado com sucesso!"
            notification = "success"

        try:
            if form.is_valid():
                if agiota:
                    form.save()
                else:
                    new_agiota = form.save(commit=False)
                    new_agiota.username = new_agiota.email
                    password = new_agiota.celular
                    new_agiota.set_password(password)
                    new_agiota.save()
        except Exception as e:
            erro = e
            msg = erro
            notification = "warning"

    context = {
        'page_title': page_title, 'form': form, 'msg': msg, 'notification': notification
    }

    return render(request, 'cadastro_agiota.html', context)


def list_agiotas(request):
    if not request.user.is_authenticated:
        return redirect('utils:acesso')

    page_title = 'Agiotas Cadastrados'
    msg = None

    agiotas = models.Agiota.objects.filter(is_active=True)

    if not agiotas:
        msg = 'Nenhum Agiota Cadastado.'

    context = {
        'msg': msg, 'agiotas': agiotas, 'page_title': page_title
    }

    return render(request, 'agiotas_cadastrados.html', context)
