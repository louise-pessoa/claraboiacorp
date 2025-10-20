from django.shortcuts import render, get_object_or_404
from .models import Noticia, Visualizacao

def index(request):
    """View para a página inicial"""
    return render(request, 'noticias/index.html')

def get_client_ip(request):
    fake_ip = request.GET.get('fake_ip')#exemplo de como testar um outro ip: http://127.0.0.1:8000/noticias/noticia_teste/?fake_ip=222.222.222.222
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

    # Cria uma visualização apenas se o IP ainda não tiver registrado essa notícia
    if not Visualizacao.objects.filter(noticia=noticia, ip_usuario=ip).exists():
        Visualizacao.objects.create(noticia=noticia, ip_usuario=ip)

    return render(request, 'noticias/detalhe.html', {'noticia': noticia})
