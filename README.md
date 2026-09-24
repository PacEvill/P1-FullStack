# Projeto 3 — Controle Financeiro

**Laboratório de Programação Full Stack (P1 — Aula 12)**  
Universidade de Vassouras — Campus Maricá  
Curso: Engenharia de Software — 6º Período  
Professor: Prof. Me. Márcio Garrido  

**Aluno:** Diego Silva Pereira Pacheco | **Matrícula:** 202413831  

---

## Sobre o Projeto

Sistema de **Controle Financeiro Pessoal** desenvolvido com Django (Python), implementando as Features obrigatórias da P1 integradas ao CRUD da disciplina (Aulas 4 a 6).

---

## Features Obrigatórias (P1 - Aula 12)

### Feature 1 — Busca Textual + Filtro por Categoria
Integrada diretamente na listagem principal de lançamentos (`/`). Combina busca textual no campo `descrição` (`descricao__icontains`) com filtro relacional por categoria via **objetos `Q()`** do ORM Django (`from django.db.models import Q`). Mantém o termo buscado no campo de busca utilizando `value="{{ request.GET.q }}"` e trata buscas vazias com `{% empty %}`.

- **Commit:** `0521b0f` — `feat(p1): Feature 1 - busca textual por descricao e filtro relacional por categoria usando objetos Q() integrados ao CRUD da listagem`

### Feature 2 — Validação Customizada no ModelForm
Implementada no `LancamentoForm` em `controle/forms.py` através de:
- `clean_valor()` — rejeita qualquer valor menor ou igual a zero (`valor <= R$ 0,00`), levantando `forms.ValidationError("O valor do lançamento deve ser maior que R$ 0,00.")`.
- `clean()` — validação cruzada que bloqueia inconsistências entre o tipo do lançamento e o tipo da categoria (ex: despesa vinculada a categoria de receita).

- **Commit:** `086ee7e` — `feat(p1): Feature 2 - validacao customizada no ModelForm: clean_valor() exige valor > 0 e clean() garante coerencia entre tipo do lancamento e tipo da categoria`

---

## Como Executar

```bash
# 1. Clone o repositório
git clone https://github.com/PacEvill/P1-FullStack.git
cd P1-FullStack

# 2. Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate   # Linux / macOS
# venv\Scripts\activate   # Windows

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Copie o arquivo de variáveis de ambiente
cp .env.example .env

# 5. Aplique as migrações do banco de dados
python manage.py migrate

# 6. (Opcional) Popule dados fictícios realistas para testes
python popular_dados.py

# 7. Inicie o servidor local
python manage.py runserver
```

Acesse em: **http://127.0.0.1:8000/**

---

## Executar Testes Automatizados

```bash
python manage.py test controle --verbosity=2
```

**20 testes automatizados** cobrindo Feature 1, Feature 2 e todas as rotas do CRUD. Resultado esperado: `OK`.

---

## Histórico Sequencial de Commits

| Commit | Tipo | Descrição |
|--------|------|-----------|
| `f1c6223` | `feat` | Configuração inicial do projeto Django com models, admin, views, templates e CRUD completo (Aula 04 e 05) |
| `0521b0f` | `feat` | Feature 1 — busca textual por descrição e filtro relacional por categoria usando objetos Q() integrados ao CRUD da listagem |
| `086ee7e` | `feat` | Feature 2 — validação customizada no ModelForm (clean_valor e clean cross-field) |
| `609dbc2` | `test` | Suíte de testes automatizados — 20 testes cobrindo Features 1 e 2 e rotas do CRUD |
| `HEAD` | `docs` | README com instruções de execução, features implementadas e tabela de commits |
