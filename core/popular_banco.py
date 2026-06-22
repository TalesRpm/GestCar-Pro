import os
import django
import random
from decimal import Decimal
from datetime import date, timedelta, time

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.models import Cliente, Veiculo, Servico, Agendamento, Comissao, Financeiro


# ==========================
# CLIENTES
# ==========================

nomes = [
    "João Silva",
    "Maria Souza",
    "Carlos Oliveira",
    "Fernanda Lima",
    "Rafael Costa",
    "Amanda Rocha",
    "Patrícia Martins",
    "Lucas Ferreira",
    "Juliana Pereira",
    "Gabriel Alves"
]

clientes = []

for i, nome in enumerate(nomes):

    cliente, _ = Cliente.objects.get_or_create(
        nome=nome,
        defaults={
            "telefone": f"(34)99999-{1000+i}",
            "email": f"cliente{i+1}@gmail.com"
        }
    )

    clientes.append(cliente)

print("Clientes criados")


# ==========================
# VEÍCULOS
# ==========================

veiculos_info = [
    ("Toyota", "Corolla", "ABC1A01", "Prata"),
    ("Honda", "Civic", "DEF2B02", "Preto"),
    ("Volkswagen", "Golf", "GHI3C03", "Branco"),
    ("Fiat", "Argo", "JKL4D04", "Vermelho"),
    ("Chevrolet", "Onix", "MNO5E05", "Cinza"),
    ("Hyundai", "HB20", "PQR6F06", "Azul"),
    ("Jeep", "Compass", "STU7G07", "Branco"),
    ("Ford", "Ka", "VWX8H08", "Prata"),
    ("Nissan", "Sentra", "YZA9I09", "Preto"),
    ("Renault", "Sandero", "BCD0J10", "Cinza")
]

veiculos = []

for cliente, dados in zip(clientes, veiculos_info):

    marca, modelo, placa, cor = dados

    veiculo, _ = Veiculo.objects.get_or_create(
        placa=placa,
        defaults={
            "cliente": cliente,
            "marca": marca,
            "modelo": modelo,
            "cor": cor
        }
    )

    veiculos.append(veiculo)

print("Veículos criados")


# ==========================
# SERVIÇOS
# ==========================

servicos_dados = [
    ("Lavagem Simples", 50, 30),
    ("Lavagem Completa", 80, 60),
    ("Higienização Interna", 150, 90),
    ("Polimento Comercial", 300, 180),
    ("Cristalização", 500, 240),
    ("Vitrificação", 1200, 360)
]

servicos = []

for nome, valor, duracao in servicos_dados:

    servico, _ = Servico.objects.get_or_create(
        nome=nome,
        defaults={
            "descricao": nome,
            "valor": Decimal(valor),
            "duracao_minutos": duracao
        }
    )

    servicos.append(servico)

print("Serviços criados")


# ==========================
# AGENDAMENTOS
# ==========================

status_lista = ["AGENDADO", "CONCLUIDO", "CANCELADO"]

for i in range(30):

    Agendamento.objects.create(
        cliente=random.choice(clientes),
        veiculo=random.choice(veiculos),
        servico=random.choice(servicos),
        data=date.today() + timedelta(days=random.randint(-10, 10)),
        hora=time(random.randint(8, 18), 0),
        status=random.choice(status_lista)
    )

print("Agendamentos criados")


# ==========================
# COMISSÕES
# ==========================

categorias = ["Lavagem", "Polimento", "Vitrificação"]

for i in range(10):

    cliente = random.choice(clientes)
    veiculo = random.choice(veiculos)

    valor_servico = Decimal(random.choice([80, 150, 300, 500]))

    Comissao.objects.create(
        cliente_nome=cliente.nome,
        telefone=cliente.telefone,
        placa=veiculo.placa,
        modelo_carro=veiculo.modelo,
        categoria=random.choice(categorias),
        servico=random.choice(categorias),
        valor_servico=valor_servico,
        comissao=valor_servico * Decimal("0.10"),
        data=date.today()
    )

print("Comissões criadas")


# ==========================
# FINANCEIRO
# ==========================

entradas = [
    ("Lavagem Completa", 80),
    ("Polimento Comercial", 300),
    ("Cristalização", 500),
    ("Vitrificação", 1200),
    ("Higienização Interna", 150)
]

saidas = [
    ("Produtos de Limpeza", 350),
    ("Energia Elétrica", 180),
    ("Marketing", 120),
    ("Água", 90),
    ("Materiais", 150)
]

for desc, valor in entradas:

    Financeiro.objects.create(
        tipo="ENTRADA",
        categoria="Serviços",
        descricao=desc,
        valor=Decimal(valor),
        forma_pagamento="PIX",
        data_movimentacao=date.today()
    )

for desc, valor in saidas:

    Financeiro.objects.create(
        tipo="SAIDA",
        categoria="Despesas",
        descricao=desc,
        valor=Decimal(valor),
        forma_pagamento="PIX",
        data_movimentacao=date.today()
    )

print("Financeiro criado")


print("\nBanco populado com sucesso!")