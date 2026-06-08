from django.contrib import admin
from .models import Cliente, Veiculo, Servico, Agendamento, Financeiro, Comissao

admin.site.register(Cliente)
admin.site.register(Veiculo)
admin.site.register(Servico)
admin.site.register(Agendamento)
admin.site.register(Financeiro)
admin.site.register(Comissao)