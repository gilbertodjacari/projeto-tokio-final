from django.contrib import admin
from .models import Veiculo, Cliente, Reserva, FormaPagamento, Contato

@admin.register(Veiculo)
class VeiculoAdmin(admin.ModelAdmin):
    list_display = ('marca', 'modelo', 'categoria', 'tipo_veiculo', 'valor_diaria', 'disponivel')
    list_filter = ('categoria', 'transmissao', 'tipo_veiculo', 'disponivel')
    search_fields = ('marca', 'modelo')
    date_hierarchy = 'data_ultima_revisao'
    fieldsets = (
        ('Informações do Veículo', {
            'fields': ('marca', 'modelo', 'categoria', 'transmissao', 'tipo_veiculo', 'capacidade_pessoas', 'imagem', 'valor_diaria', 'disponivel')
        }),
        ('Manutenção', {
            'fields': ('data_ultima_revisao', 'data_proxima_revisao', 'data_ultima_inspecao')
        }),
    )

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('user', 'telefone', 'data_registro')
    search_fields = ('user__username', 'telefone')
    list_filter = ('data_registro',)

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('veiculo', 'cliente', 'data_inicio', 'data_fim', 'valor_total', 'cancelada')
    list_filter = ('data_inicio', 'data_fim', 'cancelada')
    search_fields = ('veiculo__marca', 'veiculo__modelo', 'cliente__username')
    date_hierarchy = 'data_reserva'
    fieldsets = (
        ('Informações da Reserva', {
            'fields': ('veiculo', 'cliente', 'data_inicio', 'data_fim', 'valor_total', 'forma_pagamento', 'cancelada')
        }),
    )

@admin.register(FormaPagamento)
class FormaPagamentoAdmin(admin.ModelAdmin):
    list_display = ('tipo',)
    search_fields = ('tipo',)


@admin.register(Contato)
class ContatoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'data_envio')
    search_fields = ('nome', 'email')
    list_filter = ('data_envio',)
