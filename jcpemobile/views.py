# jcpemobile/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count, Q
from django.utils import timezone
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Noticia, Visualizacao, NoticaSalva
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
    return render(request, 'index.html', context)

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

    # Verificar se o usuário já salvou esta notícia
    noticia_salva = False
    if request.user.is_authenticated:
        noticia_salva = NoticaSalva.objects.filter(usuario=request.user, noticia=noticia).exists()

    return render(request, 'detalhes_noticia.html', {
        'noticia': noticia,
        'noticia_salva': noticia_salva
    })


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
    
    # Se não for POST, redireciona para a home (cadastro agora é apenas modal)
    return redirect('index')



def login_usuario(request):
    """View para login de usuário"""
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == 'POST':
        # Verificar se é uma requisição AJAX
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        
        # Tenta encontrar o usuário pelo email
        try:
            from django.contrib.auth.models import User
            user = User.objects.get(email=email)
            # Autentica usando o username
            user = authenticate(request, username=user.username, password=senha)
            
            if user is not None:
                login(request, user)
                if is_ajax:
                    return JsonResponse({
                        'success': True,
                        'message': 'Login realizado com sucesso!',
                        'redirect_url': '/'
                    })
                else:
                    messages.success(request, 'Login realizado com sucesso!')
                    return redirect('index')
            else:
                if is_ajax:
                    return JsonResponse({
                        'success': False,
                        'message': 'E-mail ou senha incorretos.'
                    })
                else:
                    messages.error(request, 'E-mail ou senha incorretos.')
        except User.DoesNotExist:
            if is_ajax:
                return JsonResponse({
                    'success': False,
                    'message': 'E-mail ou senha incorretos.'
                })
            else:
                messages.error(request, 'E-mail ou senha incorretos.')
    
    return redirect('index')


def logout_usuario(request):
    """View para logout de usuário"""
    logout(request)
    messages.success(request, 'Você saiu da sua conta.')
    return redirect('index')


def salvos(request):
    """View para página de notícias salvas"""
    salvos_list = []
    if request.user.is_authenticated:
        salvos_list = NoticaSalva.objects.filter(usuario=request.user).select_related('noticia', 'noticia__categoria', 'noticia__autor').order_by('-data_salvamento')
    
    return render(request, 'salvos.html', {'salvos_list': salvos_list})


def mais_lidas(request):
    """View para página de notícias mais lidas"""
    # Pegar notícias mais vistas hoje
    noticias_hoje = Noticia.objects.all().annotate(
        visualizacoes_dia=Count('visualizacoes', filter=Q(visualizacoes__data=timezone.now().date()))
    ).filter(visualizacoes_dia__gt=0).order_by('-visualizacoes_dia')
    
    # Pegar notícias mais vistas da semana
    data_semana_atras = timezone.now().date() - timezone.timedelta(days=7)
    noticias_semana = Noticia.objects.all().annotate(
        visualizacoes_semana=Count('visualizacoes', filter=Q(visualizacoes__data__gte=data_semana_atras))
    ).filter(visualizacoes_semana__gt=0).order_by('-visualizacoes_semana')
    
    # Pegar notícias mais vistas do mês
    data_mes_atras = timezone.now().date() - timezone.timedelta(days=30)
    noticias_mes = Noticia.objects.all().annotate(
        visualizacoes_mes=Count('visualizacoes', filter=Q(visualizacoes__data__gte=data_mes_atras))
    ).filter(visualizacoes_mes__gt=0).order_by('-visualizacoes_mes')
    
    context = {
        'noticias_hoje': noticias_hoje[:15],
        'noticias_semana': noticias_semana[:15],
        'noticias_mes': noticias_mes[:15],
    }
    
    return render(request, 'mais_lidas.html', context)


@login_required
@require_http_methods(["POST"])
def salvar_noticia(request, noticia_id):
    """View para salvar uma notícia"""
    noticia = get_object_or_404(Noticia, id=noticia_id)
    
    try:
        # Tenta criar o salvamento
        NoticaSalva.objects.create(usuario=request.user, noticia=noticia)
        return JsonResponse({
            'success': True,
            'message': 'Notícia salva com sucesso!',
            'salva': True
        })
    except IntegrityError:
        # Se já existe, significa que o usuário está tentando salvar novamente
        return JsonResponse({
            'success': False,
            'message': 'Você já salvou esta notícia.',
            'salva': True
        })


@login_required
@require_http_methods(["POST"])
def remover_noticia_salva(request, noticia_id):
    """View para remover uma notícia salva"""
    noticia = get_object_or_404(Noticia, id=noticia_id)
    
    try:
        noticia_salva = NoticaSalva.objects.get(usuario=request.user, noticia=noticia)
        noticia_salva.delete()
        return JsonResponse({
            'success': True,
            'message': 'Notícia removida dos salvos!',
            'salva': False
        })
    except NoticaSalva.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Esta notícia não está nos seus salvos.',
            'salva': False
        })
