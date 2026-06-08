from django.db import models


class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome


class Veiculo(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=100)
    placa = models.CharField(max_length=10)
    cor = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.modelo} - {self.placa}"


class Servico(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    valor = models.DecimalField(max_digits=8, decimal_places=2)
    duracao_minutos = models.IntegerField()

    def __str__(self):
        return self.nome


class Agendamento(models.Model):
    STATUS_CHOICES = [
        ('AGENDADO', 'Agendado'),
        ('CONCLUIDO', 'Concluído'),
        ('CANCELADO', 'Cancelado'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE)
    servico = models.ForeignKey(Servico, on_delete=models.CASCADE)
    data = models.DateField()
    hora = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='AGENDADO')

    def __str__(self):
        return f"{self.cliente} - {self.data} {self.hora}"

class Comissao(models.Model):

    cliente_nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20)

    placa = models.CharField(max_length=10)
    modelo_carro = models.CharField(max_length=100)

    categoria = models.CharField(max_length=20)
    servico = models.CharField(max_length=20)

    valor_servico = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    comissao = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)

    data = models.DateField()

    def __str__(self):
        return self.cliente_nome

class Financeiro(models.Model):

    TIPOS = (
        ('ENTRADA', 'Entrada'),
        ('SAIDA', 'Saída'),
        ('NEUTRO', 'Neutro'),
    )

    tipo = models.CharField(
        max_length=20,
        choices=TIPOS
    )

    categoria = models.CharField(max_length=100)

    descricao = models.CharField(max_length=255)

    valor = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    forma_pagamento = models.CharField(max_length=50)

    data_movimentacao = models.DateField()

    observacoes = models.TextField(
        blank=True,
        null=True
    )

    criado_em = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.descricao