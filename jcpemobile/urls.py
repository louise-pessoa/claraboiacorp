from django.urls import path
from .views import (
    noticia_detalhe, index, cadastro_usuario, login_usuario, logout_usuario,
    salvos, salvar_noticia, remover_noticia_salva, mais_lidas,
    admin_dashboard, admin_criar_noticia, admin_editar_noticia, admin_deletar_noticia
)

urlpatterns = [
    path('', index, name='index'),
    path('login/', login_usuario, name='login_usuario'),
    path('cadastro/', cadastro_usuario, name='cadastro_usuario'),
    path('logout/', logout_usuario, name='logout_usuario'),
    path('salvos/', salvos, name='salvos'),
    path('mais-lidas/', mais_lidas, name='mais_lidas'),
    path('noticia/<int:noticia_id>/salvar/', salvar_noticia, name='salvar_noticia'),
    path('noticia/<int:noticia_id>/remover/', remover_noticia_salva, name='remover_noticia_salva'),

    # Rotas de Admin (Painel Customizado)
    path('painel/', admin_dashboard, name='admin_dashboard'),
    path('painel/noticia/criar/', admin_criar_noticia, name='admin_criar_noticia'),
    path('painel/noticia/<int:noticia_id>/editar/', admin_editar_noticia, name='admin_editar_noticia'),
    path('painel/noticia/<int:noticia_id>/deletar/', admin_deletar_noticia, name='admin_deletar_noticia'),

    path('<slug:slug>/', noticia_detalhe, name='noticia_detalhe'),
]
