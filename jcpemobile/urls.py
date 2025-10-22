from django.urls import path
from .views import noticia_detalhe, index, cadastro_usuario, login_usuario, logout_usuario

urlpatterns = [
    path('', index, name='index'),
    path('login/', login_usuario, name='login_usuario'),
    path('cadastro/', cadastro_usuario, name='cadastro_usuario'),
    path('logout/', logout_usuario, name='logout_usuario'),
    path('<slug:slug>/', noticia_detalhe, name='noticia_detalhe'),
]
