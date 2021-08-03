from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from datetime import date, datetime
from . import models, forms


def confirm_emprestimo(request):
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

        if cliente and valor and juros and parcela and vencimento:
            new_emprestimo = models.Emprestimo.objects.create(valor=valor, juros=juros, num_parcela=parcela,
                                                              parcela=parcela, vencimento=vencimento,
                                                              firma=firma if firma else None)
            new_emprestimo.cliente_id = int(cliente)
            new_emprestimo.save()
            response = {
                'success': True
            }

    return JsonResponse(response, safe=True)


def open_update_emprestimo(request, pk=None):
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

    if request.method == "POST":

        if emprestimo:
            form = forms.EmprestimoForm(request.POST, instance=emprestimo)

        try:
            if form.is_valid():
                if emprestimo:
                    form.save()
                    msg = "Atualização Salva com Sucesso!"
                    notification = "success"
                    form = forms.EmprestimoForm()
        except Exception as e:
            msg = e
            notification = "warning"

    context = {
       'page_title': page_title, 'msg': msg, 'notification': notification, 'form': form, 'emprestimo': emprestimo
    }

    return render(request, 'cadastro_emprestimo.html', context)


def list_emprestimos(request):
    page_title = "Empréstimos Cadastrados"
    msg = None
    notification = None

    emprestimos = models.Emprestimo.objects.filter(is_active=True).order_by('data')

    if not emprestimos:
        msg = "Nenhum Empréstimo em Aberto"
        notification = "danger"

    context = {
        'page_title': page_title, 'msg': msg, 'notification': notification, 'emprestimos': emprestimos
    }

    return render(request, 'emprestimos_cadastrados.html', context)


@csrf_exempt
def calc_emprestimo(request):
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
    page_title = "Tabela de Cobrança"
    today = date.today()
    msg = None
    notification = None

    emprestimos = models.Emprestimo.objects.filter(vencimento=today.day, pagou_parcela=False, quitou=False)


    if not emprestimos:
        msg = "Nenhum pagamento para receber hoje!"
        notification = "success"

    context = {
        'page_title': page_title, 'emprestimos': emprestimos, 'msg': msg, 'notification': notification
    }

    return render(request, 'cobranca_diaria.html', context)


@csrf_exempt
def update_status_payment(request):
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
    page_title = "Empréstimos Quitados"

    emprestimos = models.Emprestimo.objects.filter(is_active=True, quitou=True)

    context = {
        'page_title': page_title, 'emprestimos': emprestimos
    }
    return render(request, 'emprestimos_quitados.html', context)
