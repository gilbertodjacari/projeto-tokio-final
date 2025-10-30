from django import forms
from .models import Reserva, Contato

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['data_inicio', 'data_fim', 'forma_pagamento']
        widgets = {
            'data_inicio': forms.DateInput(attrs={'type': 'date'}),
            'data_fim': forms.DateInput(attrs={'type': 'date'}),
        }



class ContatoForm(forms.ModelForm):
    class Meta:
        model = Contato
        fields = ['nome', 'email', 'mensagem']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Seu nome'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Seu email'}),
            'mensagem': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Escreva aqui...', 'style': 'height: 150px;'}),
        }
    labels = {
        'nome': 'Nome',
        'email': 'Email',
        'mensagem': 'Mensagem',
    }