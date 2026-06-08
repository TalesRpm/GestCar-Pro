from django import forms
from .models import Cliente
from .models import Veiculo
from .models import Agendamento
from django.core.exceptions import ValidationError
from .models import Servico
from .models import Comissao
from .models import Financeiro


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

class VeiculoForm(forms.ModelForm):
    class Meta:
        model = Veiculo
        fields = '__all__'
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'marca': forms.TextInput(attrs={'class': 'form-control'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control'}),
            'placa': forms.TextInput(attrs={'class': 'form-control'}),
            'cor': forms.TextInput(attrs={'class': 'form-control'}),
        }

class AgendamentoForm(forms.ModelForm):

    class Meta:
        model = Agendamento
        fields = '__all__'
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-select', 'id': 'cliente'}),
            'veiculo': forms.Select(attrs={'class': 'form-select', 'id': 'veiculo'}),
            'servico': forms.Select(attrs={'class': 'form-select'}),
            'data': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'hora': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # inicialmente nenhum veículo
        self.fields['veiculo'].queryset = Veiculo.objects.none()

        if 'cliente' in self.data:
            try:
                cliente_id = int(self.data.get('cliente'))
                self.fields['veiculo'].queryset = Veiculo.objects.filter(cliente_id=cliente_id)
            except (ValueError, TypeError):
                pass

        elif self.instance.pk:
            self.fields['veiculo'].queryset = self.instance.cliente.veiculo_set.all()
class ServicoForm(forms.ModelForm):
    class Meta:
        model = Servico
        fields = '__all__'
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control'}),
            'valor': forms.NumberInput(attrs={'class': 'form-control'}),
            'duracao_minutos': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class ComissaoForm(forms.ModelForm):

    class Meta:
        model = Comissao
        fields = '__all__'

        widgets = {

            'cliente_nome': forms.TextInput(attrs={'class':'form-control'}),
            'telefone': forms.TextInput(attrs={'class':'form-control'}),
            'placa': forms.TextInput(attrs={'class':'form-control'}),
            'modelo_carro': forms.TextInput(attrs={'class':'form-control'}),

            'categoria': forms.TextInput(attrs={'class':'form-control'}),
            'servico': forms.TextInput(attrs={'class':'form-control'}),

            'valor_servico': forms.NumberInput(attrs={
                'class':'form-control',
                'step':'0.01',
                'placeholder':'Digite manualmente se quiser'
            }),

            'comissao': forms.NumberInput(attrs={
                'class':'form-control',
                'step':'0.01',
                'placeholder':'Digite manualmente se quiser'
            }),

            'data': forms.DateInput(attrs={
                'class':'form-control',
                'type':'date'
            }),
        }

class FinanceiroForm(forms.ModelForm):

    class Meta:

        model = Financeiro

        fields = '__all__'

        widgets = {

            'tipo': forms.Select(
                attrs={'class': 'form-select'}
            ),

            'categoria': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ex: Produtos'
                }
            ),

            'descricao': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Descrição da movimentação'
                }
            ),

            'valor': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '0.00'
                }
            ),

            'forma_pagamento': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'PIX, Dinheiro, Cartão...'
                }
            ),

            'data_movimentacao': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control'
                }
            ),

            'observacoes': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4,
                    'placeholder': 'Observações adicionais'
                }
            ),
        }