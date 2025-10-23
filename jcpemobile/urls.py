from django.urls import path
from .views import (
    noticia_detalhe, index, cadastro_usuario, login_usuario, logout_usuario, 
    salvos, salvar_noticia, remover_noticia_salva, mais_lidas
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
    path('<slug:slug>/', noticia_detalhe, name='noticia_detalhe'),
]
