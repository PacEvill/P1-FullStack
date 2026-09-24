from django.urls import path
from . import views

urlpatterns = [
    # CRUD Lançamentos (Entidade Principal)
    path('', views.lista_lancamentos, name='lista_lancamentos'),
    path('lancamentos/novo/', views.novo_lancamento, name='novo_lancamento'),
    path('lancamentos/<int:pk>/', views.detalhe_lancamento, name='detalhe_lancamento'),
    path('lancamentos/<int:pk>/editar/', views.editar_lancamento, name='editar_lancamento'),
    path('lancamentos/<int:pk>/excluir/', views.excluir_lancamento, name='excluir_lancamento'),

    # CRUD Categorias
    path('categorias/', views.lista_categorias, name='lista_categorias'),
    path('categorias/nova/', views.nova_categoria, name='nova_categoria'),
    path('categorias/<int:pk>/editar/', views.editar_categoria, name='editar_categoria'),
    path('categorias/<int:pk>/excluir/', views.excluir_categoria, name='excluir_categoria'),

    # CRUD Contas
    path('contas/', views.lista_contas, name='lista_contas'),
    path('contas/nova/', views.nova_conta, name='nova_conta'),
    path('contas/<int:pk>/editar/', views.editar_conta, name='editar_conta'),
    path('contas/<int:pk>/excluir/', views.excluir_conta, name='excluir_conta'),
]
