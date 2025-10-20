from django.urls import path
from .views import noticia_detalhe, index

urlpatterns = [
    path('', index, name='index'),  # Página inicial
    path('<slug:slug>/', noticia_detalhe, name='noticia_detalhe'),
]
