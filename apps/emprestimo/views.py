from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from datetime import date, datetime
from . import models, forms


def confirm_emprestimo(request):
    if not request.user.is_authenticated:
        return redirect('utils:login')

    response = {
        'success': False
    }

    if request.method == "POST":
        firma = request.user.firma
        cliente = request.POST.get('cliente')
        valor = request.POST.get('valor')
        juros = request.POST.get('juros')
        parcela = request.POST.get('parcela')
        vencimento = request.POST.get('vencimento')
        val_parcel = request.POST.get('val_parcel')
        pk = request.POST.get('pk_', None)

        if pk:
            edit_emprestimo = models.Emprestimo.objects.get(pk=pk)
            if edit_emprestimo:
                edit_emprestimo.valor = valor
                edit_emprestimo.juros = juros
                edit_emprestimo.num_parcela = parcela
                edit_emprestimo.parcela = parcela
                edit_emprestimo.vencimento = vencimento
                edit_emprestimo.val_parcel = val_parcel
                edit_emprestimo.firma = firma if firma else None
                edit_emprestimo.save()
                response = {
                    'success': True,
                    'edit': True
                }
        else:
            if cliente and valor and juros and parcela and vencimento:
                new_emprestimo = models.Emprestimo.objects.create(valor=valor, juros=juros, num_parcela=parcela,
                                                                  parcela=parcela, vencimento=vencimento,
                                                                  val_parcel=val_parcel, firma=firma if firma else None)
                new_emprestimo.cliente_id = int(cliente)
                new_emprestimo.save()
                response = {
                    'success': True
                }

    return JsonResponse(response, safe=True)


def open_update_emprestimo(request, pk=None):
    if not request.user.is_authenticated:
        return redirect('utils:login')

    page_title = "Abertura de Empréstimo" if not pk else "Editar Empréstimo"
    msg = None
    notification = None
    form = forms.EmprestimoForm()
    emprestimo = None

    if pk:
        emprestimo = models.Emprestimo.objects.filter(pk=pk, is_active=True)
        if emprestimo:
            emprestimo = emprestimo.last()
            form = forms.EmprestimoForm(instance=emprestimo)
        else:
            msg = "Nenhum Empréstimo encontrado!"
            notification = "danger"

    context = {
       'page_title': page_title, 'msg': msg, 'notification': notification,
        'form': form, 'emprestimo': emprestimo, 'pk_': pk
    }

    return render(request, 'cadastro_emprestimo.html', context)


def list_emprestimos(request):
    if not request.user.is_authenticated:
        return redirect('utils:login')

    page_title = "Empréstimos Cadastrados"
    msg = None
    notification = None

    if request.user.is_superuser:
        emprestimos = models.Emprestimo.objects.filter(is_active=True).order_by('data')
    else:
        emprestimos = models.Emprestimo.objects.filter(is_active=True, firma=request.user.firma).order_by('data')

    if not emprestimos:
        msg = "Nenhum Empréstimo em Aberto"
        notification = "danger"

    context = {
        'page_title': page_title, 'msg': msg, 'notification': notification, 'emprestimos': emprestimos
    }

    return render(request, 'emprestimos_cadastrados.html', context)


@csrf_exempt
def calc_emprestimo(request):
    if not request.user.is_authenticated:
        return redirect('utils:login')
    response = {
        'success': False
    }

    valor_inicial = request.POST.get('valor')
    juros = request.POST.get('juros')
    meses = request.POST.get('parcela')

    if juros and meses and valor_inicial:
        juros = int(juros)
        meses = int(meses)
        valor_inicial = int(valor_inicial)

        juros = juros / 100

        x = ((1+juros)**meses)-1
        y = (juros*((1+juros)**meses))

        percentual = x/y
        parcela = valor_inicial / percentual
        valor_total = parcela * meses
        valor_juros = valor_total - valor_inicial

        response = {
            'success': True,
            'parcela': parcela,
            'valor_total': valor_total,
            'valor_juros': valor_juros,
        }

    return JsonResponse(response, safe=False)


@csrf_exempt
def detail_emprestimo(request):
    if not request.user.is_authenticated:
        return redirect('utils:login')
    response = {
        'success': False
    }

    if request.method == "POST":

        pk = request.POST.get('pk')
        if pk:

            emprestimo = models.Emprestimo.objects.get(pk=pk)

            if emprestimo:

                taxa_juros = emprestimo.juros
                meses = emprestimo.parcela
                valor_inicial = emprestimo.valor
                cliente = emprestimo.cliente.first_name

                if meses and taxa_juros and valor_inicial:
                    meses = int(meses)
                    taxa_juros = int(taxa_juros)
                    valor_inicial = int(valor_inicial)

                    juros = int(taxa_juros) / 100

                    x = ((1+juros)**meses)-1
                    y = (juros*((1+juros)**meses))

                    percentual = x/y
                    parcela = valor_inicial / percentual
                    valor_total = parcela * meses
                    valor_juros = valor_total - valor_inicial
                    qtd_parcela = valor_total/parcela

                    response = {
                        'success': True,
                        'valor_inicial': valor_inicial,
                        'valor_parcela': parcela,
                        'cliente': cliente,
                        'valor_total': valor_total,
                        'valor_juros': valor_juros,
                        'taxa_juros': taxa_juros,
                        'qtd_parcela': qtd_parcela,
                    }

    return JsonResponse(response, safe=False)


def table_charge(request):
    if not request.user.is_authenticated:
        return redirect('utils:login')
    page_title = "Tabela de Cobrança"
    today = date.today()
    msg = None
    notification = None

    if request.user.is_superuser:
        emprestimos = models.Emprestimo.objects.filter(is_active=True, vencimento=today.day, pagou_parcela=False,
                                                       quitou=False)
    else:
        emprestimos = models.Emprestimo.objects.filter(is_active=True, vencimento=today.day, pagou_parcela=False,
                                                       quitou=False,  firma=request.user.firma)

    if not emprestimos:
        msg = "Nenhum pagamento para receber hoje!"
        notification = "danger"

    context = {
        'page_title': page_title, 'emprestimos': emprestimos, 'msg': msg, 'notification': notification
    }

    return render(request, 'cobranca_diaria.html', context)


@csrf_exempt
def update_status_payment(request):
    if not request.user.is_authenticated:
        return redirect('utils:login')

    response = {'success': False}

    if request.method == 'POST':
        pk = request.POST.get('pk')

        if pk:
            emprestimo = models.Emprestimo.objects.get(pk=pk)
            if emprestimo:
                emprestimo.pagou_parcela = True
                parcelas_restante = int(emprestimo.num_parcela)
                if parcelas_restante == 1:
                    emprestimo.quitou = True
                    emprestimo.data_quitacao = datetime.now()
                    response['quitou'] = True
                else:
                    parcelas_restante -= 1
                    emprestimo.num_parcela = parcelas_restante
                    response['success'] = True
                emprestimo.save()

    return JsonResponse(response, safe=False)


def emprestimos_quitados(request):
    if not request.user.is_authenticated:
        return redirect('utils:login')

    page_title = "Empréstimos Quitados"
    notification = None
    msg = None

    if request.user.is_superuser:
        emprestimos = models.Emprestimo.objects.filter(is_active=True, quitou=True)
    else:
        emprestimos = models.Emprestimo.objects.filter(is_active=True, quitou=True, firma=request.user.firma)

    if not emprestimos:
        msg = "Nenhum Empréstimo Quitado!"
        notification = "danger"

    context = {
        'page_title': page_title, 'emprestimos': emprestimos, 'msg': msg, 'notification': notification
    }
    return render(request, 'emprestimos_quitados.html', context)


@csrf_exempt
def update_status_emprestimo(request):
    response = {
        'success': False
    }

    if request.method == 'POST':
        pk = request.POST.get('pk')

        if pk:
            emprestimo = models.Emprestimo.objects.get(pk=pk)

            if emprestimo:
                emprestimo.em_aberto = True
                emprestimo.data_em_aberto = datetime.now()
                emprestimo.save()

                response['success'] = True
    return JsonResponse(response, safe=False)


def list_emprestimo_em_aberto(request):
    page_title = 'Empréstimos em Aberto'

    emprestimos = models.Emprestimo.objects.filter(is_active=True, em_aberto=True)

    context = {
        'page_title': page_title, 'emprestimos': emprestimos
    }

    return render(request, 'emprestimos_em_aberto.html', context)