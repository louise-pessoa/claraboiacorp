# jcpemobile/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count, Q
from django.utils import timezone
from django.contrib.auth import login
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Noticia, Visualizacao
from .forms import CadastroUsuarioForm
from django.db import IntegrityError
import json

def index(request):
    """View para a página inicial"""
    noticias_mais_vistas = Noticia.objects.all().annotate(
        visualizacoes_dia=Count('visualizacoes', filter=Q(visualizacoes__data=timezone.now().date()))
    ).order_by('-visualizacoes_dia')[:5]  # Top 5 notícias do dia

    # Pegar todas as notícias para exibir na página
    todas_noticias = Noticia.objects.select_related('categoria', 'autor').order_by('-data_publicacao')

    context = {
        'noticias_mais_vistas': noticias_mais_vistas,
        'todas_noticias': todas_noticias,
    }
    return render(request, 'noticias/index.html', context)

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


@require_http_methods(["GET", "POST"])
def cadastro_usuario(request):
    """View para cadastro de novo usuário"""
    
    if request.method == 'POST':
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            try:
                data = json.loads(request.body)
                form = CadastroUsuarioForm(data)
                
                if form.is_valid():
                    user = form.save()
                    login(request, user)
                    
                    return JsonResponse({
                        'success': True,
                        'message': 'Cadastro realizado com sucesso.',
                        'redirect_url': '/'
                    })
                else:
                    errors = {}
                    for field, error_list in form.errors.items():
                        errors[field] = error_list[0] if error_list else ''
                    
                    return JsonResponse({
                        'success': False,
                        'errors': errors
                    })
            
            except json.JSONDecodeError:
                return JsonResponse({
                    'success': False,
                    'errors': {'__all__': 'Erro ao processar dados.'}
                })
            except Exception as e:
                return JsonResponse({
                    'success': False,
                    'errors': {'__all__': str(e)}
                })
        else:
            form = CadastroUsuarioForm(request.POST)
            
            if form.is_valid():
                user = form.save()
                login(request, user)
                messages.success(request, 'Cadastro realizado com sucesso.')
                return redirect('index')
            else:
                for error in form.non_field_errors():
                    messages.error(request, error)
    
    else:
        form = CadastroUsuarioForm()
    
    return render(request, 'usuario/cadastro.html', {'form': form})
