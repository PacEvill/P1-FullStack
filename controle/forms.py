from decimal import Decimal
from django import forms
from .models import Conta, Categoria, Lancamento


class ContaForm(forms.ModelForm):
    class Meta:
        model = Conta
        fields = ['nome', 'tipo', 'saldo_inicial']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Nubank, Carteira'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'saldo_inicial': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '0.00'}),
        }


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nome', 'tipo', 'descricao']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Alimentação, Salário'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descrição da categoria'}),
        }


class LancamentoForm(forms.ModelForm):
    """
    ModelForm principal para criação e edição de Lançamentos Financeiros.

    Feature 2 (P1): Validações customizadas de domínio implementadas nos
    métodos clean_valor() e clean(), garantindo integridade dos dados antes
    de qualquer operação no banco de dados.
    """

    class Meta:
        model = Lancamento
        fields = ['descricao', 'valor', 'tipo', 'data', 'conta', 'categoria', 'status', 'observacoes']
        widgets = {
            'descricao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Supermercado'}),
            'valor': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '0.00', 'min': '0.01'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'data': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'conta': forms.Select(attrs={'class': 'form-select'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Observações (opcional)'}),
        }

    # ------------------------------------------------------------------
    # Feature 2 — Validação 1: o valor do lançamento deve ser > 0
    # ------------------------------------------------------------------
    def clean_valor(self):
        """
        Regra de negócio: um lançamento financeiro NUNCA pode ter valor
        nulo ou negativo, pois representa um fluxo real de capital.
        Valores zerados corrompem o cálculo de saldo das contas.
        """
        valor = self.cleaned_data.get('valor')
        if valor is None or valor <= Decimal('0.00'):
            raise forms.ValidationError(
                "O valor do lançamento deve ser maior que R$ 0,00."
            )
        return valor

    # ------------------------------------------------------------------
    # Feature 2 — Validação 2: coerência entre tipo do lançamento e
    #             tipo da categoria selecionada (cross-field validation)
    # ------------------------------------------------------------------
    def clean(self):
        """
        Regra de negócio: a categoria de uma DESPESA deve ser do tipo DESPESA
        e a categoria de uma RECEITA deve ser do tipo RECEITA.
        A mistura invalidaria os relatórios contábeis e os limites de orçamento.
        """
        cleaned_data = super().clean()
        tipo_lancamento = cleaned_data.get('tipo')
        categoria = cleaned_data.get('categoria')

        if tipo_lancamento and categoria:
            if tipo_lancamento != categoria.tipo:
                tipo_display = 'Receita' if tipo_lancamento == 'RECEITA' else 'Despesa'
                cat_tipo_display = categoria.get_tipo_display()
                raise forms.ValidationError(
                    f"Inconsistência contábil: o lançamento é do tipo '{tipo_display}', "
                    f"mas a categoria '{categoria.nome}' é do tipo '{cat_tipo_display}'. "
                    f"Selecione uma categoria compatível com o tipo do lançamento."
                )

        return cleaned_data
