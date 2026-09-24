from django.contrib import admin
from .models import Conta, Categoria, Lancamento


@admin.register(Conta)
class ContaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo', 'saldo_inicial', 'saldo_atual', 'criado_em')
    search_fields = ('nome',)
    list_filter = ('tipo',)


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo', 'descricao')
    search_fields = ('nome', 'descricao')
    list_filter = ('tipo',)


@admin.register(Lancamento)
class LancamentoAdmin(admin.ModelAdmin):
    list_display = ('descricao', 'valor', 'tipo', 'data', 'conta', 'categoria', 'status')
    search_fields = ('descricao', 'observacoes')
    list_filter = ('tipo', 'status', 'categoria', 'conta', 'data')
    date_hierarchy = 'data'
