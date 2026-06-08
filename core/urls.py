from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [

    # HOME
    path('', views.home, name='home'),

    # CLIENTES
    path('clientes/', views.listar_clientes, name='listar_clientes'),
    path('clientes/novo/', views.cadastrar_cliente, name='cadastrar_cliente'),
    path('clientes/editar/<int:id>/', views.editar_cliente, name='editar_cliente'),
    path('clientes/excluir/<int:id>/', views.excluir_cliente, name='excluir_cliente'),

    # VEICULOS
    path('veiculos/', views.listar_veiculos, name='listar_veiculos'),
    path('veiculos/novo/', views.cadastrar_veiculo, name='cadastrar_veiculo'),

    # SERVICOS
    path('servicos/', views.listar_servicos, name='listar_servicos'),
    path('servicos/novo/', views.cadastrar_servico, name='cadastrar_servico'),
    path('servicos/editar/<int:id>/', views.editar_servico, name='editar_servico'),
    path('servicos/excluir/<int:id>/', views.excluir_servico, name='excluir_servico'),

    # AGENDAMENTOS
    path('agendamentos/', views.listar_agendamentos, name='listar_agendamentos'),
    path('agendamentos/novo/', views.cadastrar_agendamento, name='cadastrar_agendamento'),
    path('agendamentos/editar/<int:id>/', views.editar_agendamento, name='editar_agendamento'),

    path(
        'agendamentos/concluir/<int:id>/',
        views.concluir_agendamento,
        name='concluir_agendamento'
    ),

    path(
        'agendamentos/cancelar/<int:id>/',
        views.cancelar_agendamento,
        name='cancelar_agendamento'
    ),

    # CALENDARIO
    path('calendario/', views.calendario, name='calendario'),
    path('eventos/', views.eventos_agendamentos, name='eventos_agendamentos'),

    # COMISSOES
    path('comissoes/', views.listar_comissoes, name='listar_comissoes'),
    path('comissoes/nova/', views.cadastrar_comissao, name='cadastrar_comissao'),

    path(
        'comissoes/excluir/<int:id>/',
        views.excluir_comissao,
        name='excluir_comissao'
    ),

    # FINANCEIRO
    path(
        'financeiro/',
        views.listar_financeiro,
        name='listar_financeiro'
    ),

    path(
        'financeiro/novo/',
        views.criar_financeiro,
        name='criar_financeiro'
    ),

    # BUSCAS
    path('busca/', views.busca_global, name='busca_global'),
    path('busca-ajax/', views.busca_ajax, name='busca_ajax'),

    # AJAX
    path(
        'veiculos-por-cliente/<int:cliente_id>/',
        views.veiculos_por_cliente,
        name='veiculos_por_cliente'
    ),

    # LOGIN
    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='core/login.html'
        ),
        name='login'
    ),

    path(
    'logout/',
    views.logout_view,
    name='logout'
    ),

    path(
    'financeiro/pdf/',
    views.gerar_pdf_financeiro,
    name='gerar_pdf_financeiro'
),

path(
    'financeiro/editar/<int:id>/',
    views.editar_financeiro,
    name='editar_financeiro'
),

path(
    'financeiro/excluir/<int:id>/',
    views.excluir_financeiro,
    name='excluir_financeiro'
),
]