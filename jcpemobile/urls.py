from django.urls import path
from .views import noticia_detalhe

urlpatterns = [
    path('<slug:slug>/', noticia_detalhe, name='noticia_detalhe'),
]
