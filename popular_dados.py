"""
Script para popular dados ficticios para testes no Controle Financeiro (P1).
Execute via: python popular_dados.py
"""
import os
import django
from decimal import Decimal
from datetime import date, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'financeiro.settings')
django.setup()

from controle.models import Conta, Categoria, Lancamento


def run():
    print("Iniciando carga de dados fictícios para testes...")

    # Limpar lançamentos existentes
    Lancamento.objects.all().delete()
    Categoria.objects.all().delete()
    Conta.objects.all().delete()

    # 1. Contas
    conta_nubank = Conta.objects.create(nome="Nubank Principal", tipo="CORRENTE", saldo_inicial=Decimal("2500.00"))
    conta_itau = Conta.objects.create(nome="Itaú Poupança", tipo="POUPANCA", saldo_inicial=Decimal("8000.00"))
    conta_carteira = Conta.objects.create(nome="Carteira Física", tipo="CARTEIRA", saldo_inicial=Decimal("350.00"))

    # 2. Categorias de Receita e Despesa
    cat_salario = Categoria.objects.create(nome="Salário e Remuneração", tipo="RECEITA", descricao="Ganhos fixos mensais")
    cat_freelance = Categoria.objects.create(nome="Freelance / Consultoria", tipo="RECEITA", descricao="Ganhos extras e projetos")
    cat_alimentacao = Categoria.objects.create(nome="Alimentação & Mercado", tipo="DESPESA", descricao="Supermercado, feiras e restaurantes")
    cat_transporte = Categoria.objects.create(nome="Transporte & Combustível", tipo="DESPESA", descricao="Combustível, passagens e apps")
    cat_moradia = Categoria.objects.create(nome="Moradia & Contas", tipo="DESPESA", descricao="Aluguel, luz, internet e condomínio")
    cat_saude = Categoria.objects.create(nome="Saúde & Farmácia", tipo="DESPESA", descricao="Consultas, farmácia e exames")
    cat_lazer = Categoria.objects.create(nome="Lazer & Entretenimento", tipo="DESPESA", descricao="Cinema, viagens e passeios")

    # 3. Lançamentos diversos
    hoje = date.today()

    dados_lancamentos = [
        ("Salário Mensal da Empresa", Decimal("6500.00"), "RECEITA", hoje - timedelta(days=20), conta_nubank, cat_salario, "CONCLUIDO", "Depósito CLT referente ao mês"),
        ("Projeto Web Freelance", Decimal("1800.00"), "RECEITA", hoje - timedelta(days=8), conta_nubank, cat_freelance, "CONCLUIDO", "Desenvolvimento de site para cliente"),
        ("Supermercado Guanabara", Decimal("485.50"), "DESPESA", hoje - timedelta(days=15), conta_nubank, cat_alimentacao, "CONCLUIDO", "Compras do mês essenciais"),
        ("Aluguel do Apartamento", Decimal("1400.00"), "DESPESA", hoje - timedelta(days=12), conta_nubank, cat_moradia, "CONCLUIDO", "Pagamento de aluguel via Pix"),
        ("Conta de Luz Enel", Decimal("195.30"), "DESPESA", hoje - timedelta(days=10), conta_nubank, cat_moradia, "CONCLUIDO", "Fatura com débito automático"),
        ("Abastecimento Posto Ipiranga", Decimal("150.00"), "DESPESA", hoje - timedelta(days=7), conta_carteira, cat_transporte, "CONCLUIDO", "Gasolina aditivada para viagem"),
        ("Jantar Restaurante Japonês", Decimal("168.00"), "DESPESA", hoje - timedelta(days=4), conta_nubank, cat_alimentacao, "CONCLUIDO", "Comemoração familiar"),
        ("Farmácia Pacheco - Remédios", Decimal("89.90"), "DESPESA", hoje - timedelta(days=2), conta_carteira, cat_saude, "CONCLUIDO", "Medicamentos de uso contínuo"),
        ("Ingressos Cinema e Pipoca", Decimal("64.00"), "DESPESA", hoje - timedelta(days=1), conta_nubank, cat_lazer, "CONCLUIDO", "Sessão de fim de semana"),
        ("Bônus Trimestral de Metas", Decimal("1200.00"), "RECEITA", hoje, conta_itau, cat_salario, "PENDENTE", "Previsão de crédito para próxima sexta-feira"),
    ]

    for desc, val, tp, dt, cta, cat, st, obs in dados_lancamentos:
        Lancamento.objects.create(
            descricao=desc,
            valor=val,
            tipo=tp,
            data=dt,
            conta=cta,
            categoria=cat,
            status=st,
            observacoes=obs
        )

    print(f"Carga finalizada com sucesso!")
    print(f"Total de Contas: {Conta.objects.count()}")
    print(f"Total de Categorias: {Categoria.objects.count()}")
    print(f"Total de Lançamentos: {Lancamento.objects.count()}")


if __name__ == '__main__':
    run()
