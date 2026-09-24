"""
Suite de testes automatizados para o Projeto 3 - Controle Financeiro (P1).
Valida regras de negócio das Features obrigatórias e rotas do CRUD.

Execute via: python manage.py test controle
"""
from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse
from .models import Conta, Categoria, Lancamento
from .forms import LancamentoForm


class ContaModelTest(TestCase):
    """Testa o cálculo de saldo_atual da Conta."""

    def setUp(self):
        self.conta = Conta.objects.create(
            nome="Conta Teste",
            tipo="CORRENTE",
            saldo_inicial=Decimal("1000.00")
        )
        self.cat_receita = Categoria.objects.create(nome="Salário", tipo="RECEITA")
        self.cat_despesa = Categoria.objects.create(nome="Alimentação", tipo="DESPESA")

    def test_saldo_atual_com_receita(self):
        Lancamento.objects.create(
            descricao="Salário recebido", valor=Decimal("2000.00"),
            tipo="RECEITA", conta=self.conta, categoria=self.cat_receita, status="CONCLUIDO"
        )
        self.assertEqual(self.conta.saldo_atual, Decimal("3000.00"))

    def test_saldo_atual_com_despesa(self):
        Lancamento.objects.create(
            descricao="Mercado", valor=Decimal("300.00"),
            tipo="DESPESA", conta=self.conta, categoria=self.cat_despesa, status="CONCLUIDO"
        )
        self.assertEqual(self.conta.saldo_atual, Decimal("700.00"))

    def test_lancamento_pendente_nao_altera_saldo(self):
        """Lançamentos PENDENTES NÃO devem alterar o saldo_atual."""
        Lancamento.objects.create(
            descricao="Receita futura", valor=Decimal("500.00"),
            tipo="RECEITA", conta=self.conta, categoria=self.cat_receita, status="PENDENTE"
        )
        self.assertEqual(self.conta.saldo_atual, Decimal("1000.00"))


class Feature2FormValidacaoTest(TestCase):
    """
    Testa a Feature 2: validações customizadas no LancamentoForm.
    """

    def setUp(self):
        self.conta = Conta.objects.create(nome="Conta Teste", tipo="CORRENTE", saldo_inicial=Decimal("0.00"))
        self.cat_receita = Categoria.objects.create(nome="Freelance", tipo="RECEITA")
        self.cat_despesa = Categoria.objects.create(nome="Transporte", tipo="DESPESA")

    def _make_data(self, **kwargs):
        base = {
            'descricao': 'Lançamento Teste',
            'valor': '100.00',
            'tipo': 'DESPESA',
            'data': '2026-09-01',
            'conta': self.conta.pk,
            'categoria': self.cat_despesa.pk,
            'status': 'CONCLUIDO',
            'observacoes': '',
        }
        base.update(kwargs)
        return base

    def test_form_valido_despesa_com_categoria_despesa(self):
        """Lançamento DESPESA com categoria DESPESA deve ser válido."""
        form = LancamentoForm(data=self._make_data())
        self.assertTrue(form.is_valid(), form.errors)

    def test_form_valido_receita_com_categoria_receita(self):
        """Lançamento RECEITA com categoria RECEITA deve ser válido."""
        form = LancamentoForm(data=self._make_data(tipo='RECEITA', categoria=self.cat_receita.pk))
        self.assertTrue(form.is_valid(), form.errors)

    def test_clean_valor_zero_invalido(self):
        """Feature 2 — clean_valor(): valor R$0,00 deve ser rejeitado."""
        form = LancamentoForm(data=self._make_data(valor='0.00'))
        self.assertFalse(form.is_valid())
        self.assertIn('valor', form.errors)

    def test_clean_valor_negativo_invalido(self):
        """Feature 2 — clean_valor(): valor negativo deve ser rejeitado."""
        form = LancamentoForm(data=self._make_data(valor='-50.00'))
        self.assertFalse(form.is_valid())
        self.assertIn('valor', form.errors)

    def test_clean_inconsistencia_tipo_categoria(self):
        """Feature 2 — clean(): DESPESA com categoria RECEITA deve ser rejeitado."""
        form = LancamentoForm(data=self._make_data(tipo='DESPESA', categoria=self.cat_receita.pk))
        self.assertFalse(form.is_valid())
        self.assertIn('__all__', form.errors)

    def test_clean_inconsistencia_receita_com_categoria_despesa(self):
        """Feature 2 — clean(): RECEITA com categoria DESPESA deve ser rejeitado."""
        form = LancamentoForm(data=self._make_data(tipo='RECEITA', categoria=self.cat_despesa.pk))
        self.assertFalse(form.is_valid())
        self.assertIn('__all__', form.errors)


class Feature1BuscaFiltroTest(TestCase):
    """
    Testa a Feature 1: busca textual e filtro por categoria na listagem.
    """

    def setUp(self):
        self.client = Client()
        self.conta = Conta.objects.create(nome="Conta Teste", tipo="CORRENTE", saldo_inicial=Decimal("0.00"))
        self.cat_alimentacao = Categoria.objects.create(nome="Alimentação", tipo="DESPESA")
        self.cat_salario = Categoria.objects.create(nome="Salário", tipo="RECEITA")

        Lancamento.objects.create(
            descricao="Supermercado Extra", valor=Decimal("250.00"), tipo="DESPESA",
            conta=self.conta, categoria=self.cat_alimentacao, status="CONCLUIDO"
        )
        Lancamento.objects.create(
            descricao="Salário Mensal", valor=Decimal("5000.00"), tipo="RECEITA",
            conta=self.conta, categoria=self.cat_salario, status="CONCLUIDO"
        )
        Lancamento.objects.create(
            descricao="Farmácia Popular", valor=Decimal("85.00"), tipo="DESPESA",
            conta=self.conta, categoria=self.cat_alimentacao, status="PENDENTE"
        )

    def test_listagem_sem_filtro_retorna_todos(self):
        """Sem filtros, todos os lançamentos devem aparecer."""
        response = self.client.get(reverse('lista_lancamentos'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['lancamentos']), 3)

    def test_busca_textual_por_descricao(self):
        """Feature 1 — Busca textual: 'supermercado' deve retornar somente 1 resultado."""
        response = self.client.get(reverse('lista_lancamentos'), {'q': 'supermercado'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['lancamentos']), 1)
        self.assertEqual(response.context['lancamentos'][0].descricao, "Supermercado Extra")

    def test_filtro_por_categoria(self):
        """Feature 1 — Filtro por categoria: categoria 'Alimentação' deve retornar 2 lançamentos."""
        response = self.client.get(reverse('lista_lancamentos'), {'categoria': self.cat_alimentacao.pk})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['lancamentos']), 2)

    def test_busca_e_filtro_combinados(self):
        """Feature 1 — Busca + filtro simultaneamente: 'Extra' + categoria Alimentação = 1 resultado."""
        response = self.client.get(
            reverse('lista_lancamentos'),
            {'q': 'Extra', 'categoria': self.cat_alimentacao.pk}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['lancamentos']), 1)

    def test_busca_sem_resultado(self):
        """Feature 1 — Busca que não encontra nada deve retornar queryset vazia."""
        response = self.client.get(reverse('lista_lancamentos'), {'q': 'zzzinexistentezzzz'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['lancamentos']), 0)


class CRUDRotasTest(TestCase):
    """Testa se as rotas do CRUD estão acessíveis e funcional."""

    def setUp(self):
        self.client = Client()
        self.conta = Conta.objects.create(nome="Banco X", tipo="CORRENTE", saldo_inicial=Decimal("500.00"))
        self.cat = Categoria.objects.create(nome="Moradia", tipo="DESPESA")
        self.lancamento = Lancamento.objects.create(
            descricao="Aluguel", valor=Decimal("1200.00"), tipo="DESPESA",
            conta=self.conta, categoria=self.cat, status="CONCLUIDO"
        )

    def test_lista_lancamentos_status_200(self):
        response = self.client.get(reverse('lista_lancamentos'))
        self.assertEqual(response.status_code, 200)

    def test_novo_lancamento_get_status_200(self):
        response = self.client.get(reverse('novo_lancamento'))
        self.assertEqual(response.status_code, 200)

    def test_detalhe_lancamento_status_200(self):
        response = self.client.get(reverse('detalhe_lancamento', kwargs={'pk': self.lancamento.pk}))
        self.assertEqual(response.status_code, 200)

    def test_editar_lancamento_get_status_200(self):
        response = self.client.get(reverse('editar_lancamento', kwargs={'pk': self.lancamento.pk}))
        self.assertEqual(response.status_code, 200)

    def test_lista_categorias_status_200(self):
        response = self.client.get(reverse('lista_categorias'))
        self.assertEqual(response.status_code, 200)

    def test_lista_contas_status_200(self):
        response = self.client.get(reverse('lista_contas'))
        self.assertEqual(response.status_code, 200)
