from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db.models import Count, Sum, Q
from django.utils import timezone
from datetime import timedelta, date
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from datetime import datetime
from django.contrib import messages
from django.contrib.auth import logout
from .models import Cliente, Veiculo, Servico, Agendamento, Comissao, Financeiro
from .forms import ClienteForm, VeiculoForm, ServicoForm, AgendamentoForm, ComissaoForm, FinanceiroForm
from django.db.models import Sum
from .relatorios import gerar_relatorio_financeiro

# =============================
# DASHBOARD
# =============================

@login_required
def home(request):

    # =========================
    # DASHBOARD GERAL
    # =========================

    total_clientes = Cliente.objects.count()
    total_veiculos = Veiculo.objects.count()
    total_servicos = Servico.objects.count()
    total_agendamentos = Agendamento.objects.count()


    # =========================
    # STATUS AGENDAMENTOS
    # =========================

    status_data = (
        Agendamento.objects
        .values('status')
        .annotate(total=Count('status'))
    )

    status_labels = [
        item['status']
        for item in status_data
    ]

    status_totals = [
        item['total']
        for item in status_data
    ]


    # =========================
    # AGENDAMENTOS SEMANA
    # =========================

    hoje = timezone.now().date()

    sete_dias = hoje - timedelta(days=6)

    agendamentos_semana = (
        Agendamento.objects
        .filter(data__range=[sete_dias, hoje])
        .values('data')
        .annotate(total=Count('id'))
    )

    dias = []
    totais_dias = []

    for i in range(7):

        dia = sete_dias + timedelta(days=i)

        dias.append(
            dia.strftime('%d/%m')
        )

        total = next(

            (
                item['total']
                for item in agendamentos_semana
                if item['data'] == dia
            ),

            0

        )

        totais_dias.append(total)


    # =========================
    # FINANCEIRO
    # =========================

    entradas = Financeiro.objects.filter(
        tipo='ENTRADA'
    ).aggregate(
        Sum('valor')
    )['valor__sum'] or 0


    saidas = Financeiro.objects.filter(
        tipo='SAIDA'
    ).aggregate(
        Sum('valor')
    )['valor__sum'] or 0


    saldo = entradas - saidas


    # =========================
    # MOVIMENTACOES RECENTES
    # =========================

    movimentacoes = Financeiro.objects.all().order_by(
        '-data_movimentacao'
    )[:5]


    # =========================
    # AGENDAMENTOS HOJE
    # =========================

    agenda_hoje = Agendamento.objects.filter(
        data=hoje
    ).order_by('hora')[:5]


    # =========================
    # CONTEXT
    # =========================

    context = {

        'total_clientes': total_clientes,
        'total_veiculos': total_veiculos,
        'total_servicos': total_servicos,
        'total_agendamentos': total_agendamentos,

        'status_labels': status_labels,
        'status_totals': status_totals,

        'dias': dias,
        'totais_dias': totais_dias,

        'entradas': entradas,
        'saidas': saidas,
        'saldo': saldo,

        'movimentacoes': movimentacoes,

        'agenda_hoje': agenda_hoje,
    }

    return render(
        request,
        'core/home.html',
        context
    )


# =============================
# CLIENTES
# =============================

@login_required
def listar_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'core/clientes/listar.html', {'clientes': clientes})


@login_required
def cadastrar_cliente(request):

    form = ClienteForm(request.POST or None)

    if form.is_valid():
        form.save()
        messages.success(
    request,
    'Cliente cadastrado com sucesso!'
)
        return redirect('listar_clientes')

    return render(request, 'core/clientes/form.html', {'form': form})


@login_required
def editar_cliente(request, id):

    cliente = get_object_or_404(Cliente, id=id)
    form = ClienteForm(request.POST or None, instance=cliente)

    if form.is_valid():
        form.save()
        messages.success(
    request,
    'Cliente atualizado com sucesso!'
)
        return redirect('listar_clientes')

    return render(request, 'core/clientes/form.html', {'form': form})


@login_required
def excluir_cliente(request, id):

    cliente = get_object_or_404(Cliente, id=id)

    if request.method == "POST":
        cliente.delete()
        messages.success(
    request,
    'Cliente excluído com sucesso!'
)
        return redirect('listar_clientes')

    return render(request, 'core/clientes/confirmar_exclusao.html', {'cliente': cliente})


# =============================
# VEÍCULOS
# =============================

@login_required
def listar_veiculos(request):

    veiculos = Veiculo.objects.select_related('cliente').all()

    return render(request, 'core/veiculos/listar.html', {
        'veiculos': veiculos
    })


@login_required
def cadastrar_veiculo(request):

    form = VeiculoForm(request.POST or None)

    if form.is_valid():

        form.save()

        messages.success(
            request,
            'Veículo cadastrado com sucesso!'
        )

        return redirect('listar_veiculos')

    return render(
        request,
        'core/veiculos/form.html',
        {
            'form': form
        }
    )
    
@login_required
def editar_veiculo(request, id):

    veiculo = get_object_or_404(
        Veiculo,
        id=id
    )

    form = VeiculoForm(
        request.POST or None,
        instance=veiculo
    )

    if form.is_valid():

        form.save()

        messages.success(
            request,
            'Veículo atualizado com sucesso!'
        )

        return redirect(
            'listar_veiculos'
        )

    return render(
        request,
        'core/veiculos/form.html',
        {
            'form': form
        }
    )


@login_required
def excluir_veiculo(request, id):

    veiculo = get_object_or_404(
        Veiculo,
        id=id
    )

    if request.method == 'POST':

        veiculo.delete()

        messages.success(
            request,
            'Veículo excluído com sucesso!'
        )

        return redirect(
            'listar_veiculos'
        )

    return render(
        request,
        'core/veiculos/confirmar_exclusao.html',
        {
            'veiculo': veiculo
        }
    )


# =============================
# AGENDAMENTOS
# =============================

@login_required
def listar_agendamentos(request):

    agendamentos = Agendamento.objects.select_related(
        'cliente',
        'veiculo',
        'servico'
    ).all()


    # =========================
    # FILTROS
    # =========================

    busca = request.GET.get('busca')

    status = request.GET.get('status')

    data = request.GET.get('data')


    # BUSCA

    if busca:

        agendamentos = agendamentos.filter(
            cliente__nome__icontains=busca
        )


    # STATUS

    if status:

        agendamentos = agendamentos.filter(
            status=status
        )


    # DATA

    if data:

        agendamentos = agendamentos.filter(
            data=data
        )


    return render(

        request,

        'core/agendamentos/listar.html',

        {

            'agendamentos': agendamentos

        }

    )


@login_required
def cadastrar_agendamento(request):

    form = AgendamentoForm(request.POST or None)

    if form.is_valid():

        form.save()

        messages.success(
            request,
            'Agendamento criado com sucesso!'
        )

        return redirect(
            'listar_agendamentos'
        )

    return render(
        request,
        'core/agendamentos/form.html',
        {
            'form': form
        }
    )


@login_required
def editar_agendamento(request, id):

    agendamento = get_object_or_404(
        Agendamento,
        id=id
    )

    form = AgendamentoForm(
        request.POST or None,
        instance=agendamento
    )

    if form.is_valid():

        form.save()

        messages.success(
            request,
            'Agendamento atualizado com sucesso!'
        )

        return redirect(
            'listar_agendamentos'
        )

    return render(
        request,
        'core/agendamentos/form.html',
        {
            'form': form
        }
    )


@login_required
def concluir_agendamento(request, id):

    agendamento = get_object_or_404(Agendamento, id=id)

    agendamento.status = "CONCLUIDO"
    agendamento.save()

    messages.success(
    request,
    'Agendamento concluído!'
)

    return redirect('listar_agendamentos')


@login_required
def cancelar_agendamento(request, id):

    agendamento = get_object_or_404(Agendamento, id=id)

    agendamento.status = "CANCELADO"
    agendamento.save()

    messages.success(
    request,
    'Agendamento cancelado!'
)

    return redirect('listar_agendamentos')


# =============================
# SERVIÇOS
# =============================

@login_required
def listar_servicos(request):

    servicos = Servico.objects.all()

    return render(request, 'core/servicos/listar.html', {
        'servicos': servicos
    })


@login_required
def cadastrar_servico(request):

    form = ServicoForm(request.POST or None)

    if form.is_valid():

        form.save()

        messages.success(
            request,
            'Serviço cadastrado com sucesso!'
        )

        return redirect(
            'listar_servicos'
        )

    return render(
        request,
        'core/servicos/form.html',
        {
            'form': form
        }
    )


@login_required
def editar_servico(request, id):

    servico = get_object_or_404(
        Servico,
        id=id
    )

    form = ServicoForm(
        request.POST or None,
        instance=servico
    )

    if form.is_valid():

        form.save()

        messages.success(
            request,
            'Serviço atualizado com sucesso!'
        )

        return redirect(
            'listar_servicos'
        )

    return render(
        request,
        'core/servicos/form.html',
        {
            'form': form
        }
    )

@login_required
def excluir_servico(request, id):

    servico = get_object_or_404(Servico, id=id)

    if request.method == "POST":
        servico.delete()
        messages.success(
    request,
    'Serviço excluído com sucesso!'
)
        return redirect('listar_servicos')

    return render(request, 'core/servicos/confirmar_exclusao.html', {
        'servico': servico
    })


# =============================
# CALENDÁRIO
# =============================

@login_required
def calendario(request):
    return render(request, 'core/agendamentos/calendario.html')


@login_required
def eventos_agendamentos(request):

    agendamentos = Agendamento.objects.select_related(
        'cliente',
        'veiculo',
        'servico'
    ).all()

    eventos = []

    for a in agendamentos:

        eventos.append({
            "id": a.id,
            "title": a.cliente.nome,
            "start": f"{a.data}T{a.hora}",
            "extendedProps": {
                "cliente": a.cliente.nome,
                "veiculo": f"{a.veiculo.modelo} - {a.veiculo.placa}",
                "servico": a.servico.nome,
                "status": a.status
            },
            "color": "#dc2626" if a.status == "AGENDADO" else "#16a34a"
        })

    return JsonResponse(eventos, safe=False)


# =============================
# VEÍCULOS POR CLIENTE
# =============================

def veiculos_por_cliente(request, cliente_id):

    veiculos = Veiculo.objects.filter(cliente_id=cliente_id)

    lista = []

    for v in veiculos:

        lista.append({
            'id': v.id,
            'nome': f"{v.marca} {v.modelo} - {v.placa}"
        })

    return JsonResponse(lista, safe=False)


# =============================
# COMISSÕES
# =============================

def calcular_valores(categoria, servico):

    tabela = {

        ('popular','sem_cera'): (70, 1.30),
        ('popular','com_cera'): (90, 2.00),

        ('suv','sem_cera'): (80, 1.80),
        ('suv','com_cera'): (100, 2.50),

        ('caminhonete','sem_cera'): (120, 3.00),
        ('caminhonete','com_cera'): (150, 5.00),

    }

    return tabela.get((categoria, servico), (0,0))


def listar_comissoes(request):

    comissoes = Comissao.objects.all().order_by('-data')

    hoje = date.today()

    comissao_hoje = Comissao.objects.filter(
        data=hoje
    ).aggregate(total=Sum('comissao'))['total'] or 0

    comissao_mes = Comissao.objects.filter(
        data__month=hoje.month
    ).aggregate(total=Sum('comissao'))['total'] or 0

    total_servicos = Comissao.objects.count()

    return render(request, 'core/comissoes/listar.html', {
        'comissoes': comissoes,
        'comissao_hoje': comissao_hoje,
        'comissao_mes': comissao_mes,
        'total_servicos': total_servicos
    })


def cadastrar_comissao(request):

    form = ComissaoForm(request.POST or None)

    if form.is_valid():

        comissao = form.save(commit=False)

        # Se os campos estiverem vazios, calcula automaticamente
        if not comissao.valor_servico or not comissao.comissao:

            valor, valor_comissao = calcular_valores(
                comissao.categoria,
                comissao.servico
            )

            if not comissao.valor_servico:
                comissao.valor_servico = valor

            if not comissao.comissao:
                comissao.comissao = valor_comissao

        comissao.save()

        messages.success(
    request,
    'Comissão cadastrada com sucesso!'
)

        return redirect('listar_comissoes')

    return render(request, 'core/comissoes/form.html', {
        'form': form
    })


# =============================
# BUSCA GLOBAL
# =============================

def busca_global(request):

    query = request.GET.get('q')

    clientes = []
    veiculos = []

    if query:

        clientes = Cliente.objects.filter(
            Q(nome__icontains=query) |
            Q(telefone__icontains=query) |
            Q(email__icontains=query)
        )

        veiculos = Veiculo.objects.filter(
            Q(placa__icontains=query) |
            Q(modelo__icontains=query) |
            Q(marca__icontains=query)
        )

    return render(request, 'core/busca.html', {
        'query': query,
        'clientes': clientes,
        'veiculos': veiculos
    })


def busca_ajax(request):

    query = request.GET.get("q", "")

    clientes = []
    veiculos = []

    if query:

        clientes_qs = Cliente.objects.filter(
            Q(nome__icontains=query) |
            Q(telefone__icontains=query)
        )[:5]

        veiculos_qs = Veiculo.objects.filter(
            Q(placa__icontains=query) |
            Q(modelo__icontains=query)
        )[:5]

        clientes = [
            {
                "id": c.id,
                "nome": c.nome,
                "telefone": c.telefone
            }
            for c in clientes_qs
        ]

        veiculos = [
            {
                "id": v.id,
                "placa": v.placa,
                "modelo": v.modelo,
                "cliente": v.cliente.nome
            }
            for v in veiculos_qs
        ]

    return JsonResponse({
        "clientes": clientes,
        "veiculos": veiculos
    })
    
@login_required
def editar_comissao(request, id):

    comissao = get_object_or_404(
        Comissao,
        id=id
    )

    form = ComissaoForm(
        request.POST or None,
        instance=comissao
    )

    if form.is_valid():

        comissao = form.save(commit=False)

        # Recalcula automaticamente apenas se os campos estiverem vazios
        if not comissao.valor_servico or not comissao.comissao:

            valor, valor_comissao = calcular_valores(
                comissao.categoria,
                comissao.servico
            )

            if not comissao.valor_servico:
                comissao.valor_servico = valor

            if not comissao.comissao:
                comissao.comissao = valor_comissao

        comissao.save()

        messages.success(
            request,
            'Comissão atualizada com sucesso!'
        )

        return redirect(
            'listar_comissoes'
        )

    return render(
        request,
        'core/comissoes/form.html',
        {
            'form': form
        }
    )

def excluir_comissao(request, id):

    comissao = get_object_or_404(Comissao, id=id)

    if request.method == "POST":
        comissao.delete()
        messages.success(
    request,
    'Comissão excluída com sucesso!'
)
        return redirect('listar_comissoes')

    return render(request, 'core/comissoes/confirmar_exclusao.html', {
        'comissao': comissao
    })

@login_required
def listar_financeiro(request):

    financeiro = Financeiro.objects.all().order_by(
        '-data_movimentacao'
    )


    # =========================
    # FILTROS
    # =========================

    tipo = request.GET.get('tipo')
    categoria = request.GET.get('categoria')
    forma_pagamento = request.GET.get('forma_pagamento')
    busca = request.GET.get('busca')

    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')


    if tipo:

        financeiro = financeiro.filter(
            tipo=tipo
        )


    if categoria:

        financeiro = financeiro.filter(
            categoria__icontains=categoria
        )

    if forma_pagamento:

        financeiro = financeiro.filter(
            forma_pagamento__icontains=forma_pagamento
    )

    if busca:

        financeiro = financeiro.filter(
            descricao__icontains=busca
        )


    if data_inicio:

        financeiro = financeiro.filter(
            data_movimentacao__gte=data_inicio
        )


    if data_fim:

        financeiro = financeiro.filter(
            data_movimentacao__lte=data_fim
        )


    # =========================
    # RESUMO FINANCEIRO
    # =========================

    entradas = financeiro.filter(
        tipo='ENTRADA'
    ).aggregate(
        Sum('valor')
    )['valor__sum'] or 0


    saidas = financeiro.filter(
        tipo='SAIDA'
    ).aggregate(
        Sum('valor')
    )['valor__sum'] or 0


    saldo = entradas - saidas


    # =========================
    # GRAFICO ENTRADAS X SAIDAS
    # =========================

    grafico_labels = [
        'Entradas',
        'Saídas'
    ]

    grafico_valores = [
        float(entradas),
        float(saidas)
    ]


    # =========================
    # GRAFICO MENSAL
    # =========================

    meses = [
        'Jan', 'Fev', 'Mar', 'Abr',
        'Mai', 'Jun', 'Jul', 'Ago',
        'Set', 'Out', 'Nov', 'Dez'
    ]

    faturamento_mensal = []

    for mes in range(1, 13):

        total = Financeiro.objects.filter(
            tipo='ENTRADA',
            data_movimentacao__month=mes
        ).aggregate(
            Sum('valor')
        )['valor__sum'] or 0

        faturamento_mensal.append(
            float(total)
        )


    return render(

        request,

        'core/financeiro/listar.html',

        {

            'financeiro': financeiro,

            'entradas': entradas,
            'saidas': saidas,
            'saldo': saldo,

            'grafico_labels': grafico_labels,
            'grafico_valores': grafico_valores,

            'faturamento_mensal': faturamento_mensal,
            'meses': meses,
        }

    )

@login_required
def criar_financeiro(request):

    form = FinanceiroForm(
        request.POST or None
    )

    if form.is_valid():

        form.save()

        messages.success(
            request,
            'Movimentação cadastrada com sucesso!'
        )

        return redirect(
            'listar_financeiro'
        )

    return render(
        request,
        'core/financeiro/form.html',
        {
            'form': form
        }
    )

@login_required
def gerar_pdf_financeiro(request):
    return gerar_relatorio_financeiro(request)

@login_required
def editar_financeiro(request, id):

    movimentacao = get_object_or_404(
        Financeiro,
        id=id
    )

    form = FinanceiroForm(
        request.POST or None,
        instance=movimentacao
    )

    if form.is_valid():

        form.save()

        messages.success(
            request,
            'Movimentação atualizada com sucesso!'
        )

        return redirect('listar_financeiro')

    return render(
        request,
        'core/financeiro/form.html',
        {
            'form': form
        }
    )
    
@login_required
def excluir_financeiro(request, id):

    movimentacao = get_object_or_404(
        Financeiro,
        id=id
    )

    if request.method == 'POST':

        movimentacao.delete()

        messages.success(
    request,
    'Movimentação excluída com sucesso!'
)

        return redirect(
            'listar_financeiro'
        )

    return render(
        request,
        'core/financeiro/confirmar_exclusao.html',
        {
            'movimentacao': movimentacao
        }
    )
    
def logout_view(request):

    logout(request)

    return redirect('login')