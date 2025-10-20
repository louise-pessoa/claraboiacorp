# jcpemobile/views.py
from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Q
from django.utils import timezone
from .models import Noticia, Visualizacao
from django.db import IntegrityError

def index(request):
    """View para a página inicial"""
    noticias_mais_vistas = Noticia.objects.all().annotate(
        visualizacoes_dia=Count('visualizacoes', filter=Q(visualizacoes__data=timezone.now().date()))
    ).order_by('-visualizacoes_dia')[:5]  # Top 5 notícias do dia
    return render(request, 'noticias/index.html', {'noticias_mais_vistas': noticias_mais_vistas})

def get_client_ip(request):
    fake_ip = request.GET.get('fake_ip')  # Exemplo: http://127.0.0.1:8000/noticias/noticia_teste/?fake_ip=222.222.222.222
    if fake_ip:
        return fake_ip

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def noticia_detalhe(request, slug):
    noticia = get_object_or_404(Noticia, slug=slug)
    ip = get_client_ip(request)

    # Cria uma visualização apenas se o IP ainda não tiver registrado essa notícia hoje
    if not Visualizacao.objects.filter(noticia=noticia, ip_address=ip, data=timezone.now().date()).exists():
        Visualizacao.objects.create(
            noticia=noticia,
            ip_address=ip,
            data=timezone.now().date()  # Set the date field
        )

    return render(request, 'noticias/detalhes_noticia.html', {'noticia': noticia})