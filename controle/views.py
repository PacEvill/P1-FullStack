from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Conta, Categoria, Lancamento
from .forms import ContaForm, CategoriaForm, LancamentoForm


# ==============================================================================
# CRUD DE LANÇAMENTOS (Entidade Principal)
# ==============================================================================

def lista_lancamentos(request):
    """
    Listagem principal de lançamentos financeiros (CRUD existente - Aula 05).

    Feature 1 (P1): Busca textual por descrição e filtro relacional por
    categoria, combinados via objetos Q() do ORM do Django.
    Ambos os filtros operam simultaneamente na mesma queryset/tabela.
    """
    lancamentos = Lancamento.objects.all().select_related('conta', 'categoria')
    categorias = Categoria.objects.all()

    # --- Feature 1: Busca textual por descrição ---
    q = request.GET.get('q', '').strip()
    if q:
        lancamentos = lancamentos.filter(
            Q(descricao__icontains=q) | Q(observacoes__icontains=q)
        )

    # --- Feature 1: Filtro relacional por categoria ---
    categoria_id = request.GET.get('categoria', '').strip()
    if categoria_id:
        lancamentos = lancamentos.filter(categoria__id=categoria_id)

    return render(request, 'controle/lancamentos_lista.html', {
        'lancamentos': lancamentos,
        'categorias': categorias,
        'q': q,
        'categoria_id': categoria_id,
    })


def novo_lancamento(request):
    """Criação de um novo lançamento financeiro."""
    if request.method == 'POST':
        form = LancamentoForm(request.POST)
        if form.is_valid():
            lancamento = form.save()
            messages.success(request, f"Lançamento '{lancamento.descricao}' cadastrado com sucesso!")
            return redirect('lista_lancamentos')
    else:
        form = LancamentoForm()

    return render(request, 'controle/form.html', {
        'form': form,
        'titulo': 'Novo Lançamento',
        'subtitulo': 'Cadastre uma nova movimentação de receita ou despesa',
        'btn_texto': 'Salvar Lançamento',
    })


def editar_lancamento(request, pk):
    """Edição de um lançamento financeiro existente."""
    lancamento = get_object_or_404(Lancamento, pk=pk)
    if request.method == 'POST':
        form = LancamentoForm(request.POST, instance=lancamento)
        if form.is_valid():
            form.save()
            messages.success(request, f"Lançamento '{lancamento.descricao}' atualizado com sucesso!")
            return redirect('lista_lancamentos')
    else:
        form = LancamentoForm(instance=lancamento)

    return render(request, 'controle/form.html', {
        'form': form,
        'titulo': f'Editar: {lancamento.descricao}',
        'subtitulo': 'Atualize os dados deste lançamento financeiro',
        'btn_texto': 'Salvar Alterações',
    })


def excluir_lancamento(request, pk):
    """Exclusão de um lançamento financeiro com confirmação."""
    lancamento = get_object_or_404(Lancamento, pk=pk)
    if request.method == 'POST':
        descricao = lancamento.descricao
        lancamento.delete()
        messages.success(request, f"Lançamento '{descricao}' excluído com sucesso!")
        return redirect('lista_lancamentos')

    return render(request, 'controle/confirmar_exclusao.html', {
        'objeto': lancamento,
        'tipo_objeto': 'Lançamento',
        'url_cancelar': 'lista_lancamentos',
    })


def detalhe_lancamento(request, pk):
    """Exibição detalhada de um lançamento específico."""
    lancamento = get_object_or_404(Lancamento.objects.select_related('conta', 'categoria'), pk=pk)
    return render(request, 'controle/lancamento_detalhe.html', {
        'lancamento': lancamento,
    })


# ==============================================================================
# CRUD DE CATEGORIAS
# ==============================================================================

def lista_categorias(request):
    """Listagem de todas as categorias cadastradas."""
    categorias = Categoria.objects.all()
    return render(request, 'controle/categorias_lista.html', {
        'categorias': categorias,
    })


def nova_categoria(request):
    """Criação de uma nova categoria."""
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            categoria = form.save()
            messages.success(request, f"Categoria '{categoria.nome}' cadastrada com sucesso!")
            return redirect('lista_categorias')
    else:
        form = CategoriaForm()

    return render(request, 'controle/form.html', {
        'form': form,
        'titulo': 'Nova Categoria',
        'subtitulo': 'Classifique receitas e despesas com novas categorias',
        'btn_texto': 'Salvar Categoria',
    })


def editar_categoria(request, pk):
    """Edição de uma categoria existente."""
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, f"Categoria '{categoria.nome}' atualizada com sucesso!")
            return redirect('lista_categorias')
    else:
        form = CategoriaForm(instance=categoria)

    return render(request, 'controle/form.html', {
        'form': form,
        'titulo': f'Editar Categoria: {categoria.nome}',
        'subtitulo': 'Atualize os dados desta categoria',
        'btn_texto': 'Salvar Alterações',
    })


def excluir_categoria(request, pk):
    """Exclusão de uma categoria com confirmação."""
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        nome = categoria.nome
        categoria.delete()
        messages.success(request, f"Categoria '{nome}' excluída com sucesso!")
        return redirect('lista_categorias')

    return render(request, 'controle/confirmar_exclusao.html', {
        'objeto': categoria,
        'tipo_objeto': 'Categoria',
        'url_cancelar': 'lista_categorias',
    })


# ==============================================================================
# CRUD DE CONTAS
# ==============================================================================

def lista_contas(request):
    """Listagem de contas bancárias e carteiras."""
    contas = Conta.objects.all()
    return render(request, 'controle/contas_lista.html', {
        'contas': contas,
    })


def nova_conta(request):
    """Criação de uma nova conta."""
    if request.method == 'POST':
        form = ContaForm(request.POST)
        if form.is_valid():
            conta = form.save()
            messages.success(request, f"Conta '{conta.nome}' criada com sucesso!")
            return redirect('lista_contas')
    else:
        form = ContaForm()

    return render(request, 'controle/form.html', {
        'form': form,
        'titulo': 'Nova Conta',
        'subtitulo': 'Cadastre contas correntes, carteiras e investimentos',
        'btn_texto': 'Salvar Conta',
    })


def editar_conta(request, pk):
    """Edição de uma conta existente."""
    conta = get_object_or_404(Conta, pk=pk)
    if request.method == 'POST':
        form = ContaForm(request.POST, instance=conta)
        if form.is_valid():
            form.save()
            messages.success(request, f"Conta '{conta.nome}' atualizada com sucesso!")
            return redirect('lista_contas')
    else:
        form = ContaForm(instance=conta)

    return render(request, 'controle/form.html', {
        'form': form,
        'titulo': f'Editar Conta: {conta.nome}',
        'subtitulo': 'Atualize os dados da conta financeira',
        'btn_texto': 'Salvar Alterações',
    })


def excluir_conta(request, pk):
    """Exclusão de uma conta com confirmação."""
    conta = get_object_or_404(Conta, pk=pk)
    if request.method == 'POST':
        nome = conta.nome
        conta.delete()
        messages.success(request, f"Conta '{nome}' excluída com sucesso!")
        return redirect('lista_contas')

    return render(request, 'controle/confirmar_exclusao.html', {
        'objeto': conta,
        'tipo_objeto': 'Conta',
        'url_cancelar': 'lista_contas',
    })
