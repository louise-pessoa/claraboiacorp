from django.urls import path
from .views import noticia_detalhe, index, cadastro_usuario

urlpatterns = [
    path('', index, name='index'),
    path('cadastro/', cadastro_usuario, name='cadastro_usuario'),
    path('<slug:slug>/', noticia_detalhe, name='noticia_detalhe'),
]
