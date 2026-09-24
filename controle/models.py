from decimal import Decimal
from django.db import models
from django.db.models import Sum
from django.utils import timezone


class Conta(models.Model):
    """
    Entidade 1: Conta Financeira
    Representa a instituição ou local de custódia (ex: Nubank, Itaú, Carteira).
    """
    TIPOS_CONTA = [
        ('CORRENTE', 'Conta Corrente'),
        ('POUPANCA', 'Poupança'),
        ('INVESTIMENTO', 'Investimento'),
        ('CARTEIRA', 'Dinheiro em Espécie / Carteira'),
    ]

    nome = models.CharField(max_length=100, verbose_name="Nome da Conta")
    tipo = models.CharField(max_length=20, choices=TIPOS_CONTA, default='CORRENTE', verbose_name="Tipo de Conta")
    saldo_inicial = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'), verbose_name="Saldo Inicial (R$)")
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")

    class Meta:
        verbose_name = "Conta"
        verbose_name_plural = "Contas"
        ordering = ['nome']

    def __str__(self):
        return f"{self.nome} ({self.get_tipo_display()})"

    @property
    def saldo_atual(self):
        """Calcula o saldo atual: Saldo Inicial + Receitas Concluídas - Despesas Concluídas."""
        receitas = self.lancamentos.filter(tipo='RECEITA', status='CONCLUIDO').aggregate(total=Sum('valor'))['total'] or Decimal('0.00')
        despesas = self.lancamentos.filter(tipo='DESPESA', status='CONCLUIDO').aggregate(total=Sum('valor'))['total'] or Decimal('0.00')
        return self.saldo_inicial + receitas - despesas


class Categoria(models.Model):
    """
    Entidade 2: Categoria Financeira
    Classifica receitas e despesas (ex: Alimentação, Moradia, Salário).
    """
    TIPOS_CATEGORIA = [
        ('RECEITA', 'Receita (+)'),
        ('DESPESA', 'Despesa (-)'),
    ]

    nome = models.CharField(max_length=100, verbose_name="Nome da Categoria")
    tipo = models.CharField(max_length=10, choices=TIPOS_CATEGORIA, default='DESPESA', verbose_name="Tipo de Categoria")
    descricao = models.TextField(blank=True, verbose_name="Descrição / Observações")

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        ordering = ['tipo', 'nome']

    def __str__(self):
        return f"{self.nome} [{self.get_tipo_display()}]"


class Lancamento(models.Model):
    """
    Entidade 3: Lançamento Financeiro (Transação Principal)
    Registra entradas e saídas de valores do sistema.
    """
    TIPOS_LANCAMENTO = [
        ('RECEITA', 'Receita (+)'),
        ('DESPESA', 'Despesa (-)'),
    ]

    STATUS_CHOICES = [
        ('CONCLUIDO', 'Concluído / Pago'),
        ('PENDENTE', 'Pendente / A Vencer'),
    ]

    descricao = models.CharField(max_length=150, verbose_name="Descrição do Lançamento")
    valor = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Valor (R$)")
    tipo = models.CharField(max_length=10, choices=TIPOS_LANCAMENTO, default='DESPESA', verbose_name="Tipo")
    data = models.DateField(default=timezone.now, verbose_name="Data do Lançamento")
    conta = models.ForeignKey(Conta, on_delete=models.CASCADE, related_name="lancamentos", verbose_name="Conta")
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name="lancamentos", verbose_name="Categoria")
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='CONCLUIDO', verbose_name="Status")
    observacoes = models.TextField(blank=True, verbose_name="Observações")
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")

    class Meta:
        verbose_name = "Lançamento"
        verbose_name_plural = "Lançamentos"
        ordering = ['-data', '-id']

    def __str__(self):
        sinal = "+" if self.tipo == 'RECEITA' else "-"
        return f"{self.descricao} | {sinal}R$ {self.valor:.2f} ({self.data.strftime('%d/%m/%Y')})"
