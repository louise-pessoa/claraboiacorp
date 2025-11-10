# jcpemobile/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count, Q
from django.utils import timezone
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Noticia, Visualizacao, NoticaSalva, Categoria, Autor, Feedback, Enquete, Voto, Opcao
from .forms import CadastroUsuarioForm, NoticiaForm, FeedbackForm
from django.db import IntegrityError
import json

def get_client_ip(request):
    fake_ip_post = request.POST.get('fake_ip')
    if fake_ip_post:
        return fake_ip_post

    fake_ip = request.GET.get('fake_ip')  # Exemplo: http://127.0.0.1:8000/noticias/noticia_teste/?fake_ip=222.222.222.222
    if fake_ip:
        return fake_ip

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def index(request):
    """View para a página inicial"""
    hoje = timezone.now().date()
    # Busca as notícias mais vistas do dia, com ordenamento secundário por data de publicação
    noticias_mais_vistas = Noticia.objects.all().annotate(
        visualizacoes_dia=Count('visualizacoes', filter=Q(visualizacoes__data=hoje))
    ).order_by('-visualizacoes_dia', '-data_publicacao')[:9]  # Top 10 notícias do dia

    # Pegar todas as notícias para exibir na página
    todas_noticias = Noticia.objects.select_related('categoria', 'autor').order_by('-data_publicacao')

    context = {
        'noticias_mais_vistas': noticias_mais_vistas,
        'todas_noticias': todas_noticias,
    }
    return render(request, 'index.html', context)

# Página com todas as enquetes
def lista_enquetes(request):
    enquetes = Enquete.objects.all()
    return render(request, 'enquetes.html', {'enquetes': enquetes})


# Página de detalhe/votação de uma enquete
def detalhe_enquete(request, enquete_id):
    enquete = get_object_or_404(Enquete, id=enquete_id)

    # IMPORTANT: get_client_ip agora lê POST/GET fake_ip também
    ip_usuario = get_client_ip(request)
    ja_votou = Voto.objects.filter(opcao__enquete=enquete, ip_usuario=ip_usuario).exists()

    if request.method == 'POST':
        if ja_votou:
            # avisar que já votou
            messages.warning(request, "Você já votou nesta enquete com o IP atual.")
        else:
            opcao_id = request.POST.get('opcao')
            # validação adicional: opcao_id existe
            opcao = get_object_or_404(Opcao, id=opcao_id, enquete=enquete)
            Voto.objects.create(opcao=opcao, ip_usuario=ip_usuario)
            messages.success(request, "Voto registrado com sucesso!")
        # redireciona para a mesma página para evitar reenvio de formulário
        # preservando querystring (ex.: ?fake_ip=1.2.3.4) para conveniência de testes
        redirect_url = request.path
        qs = request.META.get('QUERY_STRING')
        if qs:
            redirect_url = f"{redirect_url}?{qs}"
        return redirect(redirect_url)

    opcoes = enquete.opcoes.all()
    total_votos = enquete.total_votos()

    contexto = {
        'enquete': enquete,
        'opcoes': opcoes,
        'total_votos': total_votos,
        'ja_votou': ja_votou,
    }

    return render(request, 'detalhe_enquete.html', contexto)


def neels(request):
    """View para a página Neels"""
    # Pegar todas as notícias ordenadas por data de publicação
    noticias = Noticia.objects.select_related('categoria', 'autor').order_by('-data_publicacao')
    
    context = {
        'noticias': noticias,
    }
    return render(request, 'neels.html', context)

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

    # Processar votação da enquete se houver
    ja_votou_enquete = False
    enquete = None
    if hasattr(noticia, 'enquete'):
        enquete = noticia.enquete

        # Verificar se já votou
        ja_votou_enquete = Voto.objects.filter(
            opcao__enquete=enquete,
            ip_usuario=ip
        ).exists()

        # Processar voto se for POST
        if request.method == 'POST' and not ja_votou_enquete:
            opcao_id = request.POST.get('opcao_id')
            if opcao_id:
                try:
                    opcao = Opcao.objects.get(id=opcao_id, enquete=enquete)
                    Voto.objects.create(opcao=opcao, ip_usuario=ip)
                    ja_votou_enquete = True
                    messages.success(request, 'Voto registrado com sucesso!')
                    return redirect('noticia_detalhe', slug=slug)
                except Opcao.DoesNotExist:
                    messages.error(request, 'Opção inválida.')
        elif request.method == 'POST' and ja_votou_enquete:
            messages.warning(request, 'Você já votou nesta enquete.')

    # Buscar notícias relacionadas
    noticias_relacionadas = []
    if noticia.categoria:
        # Buscar notícias da mesma categoria, excluindo a notícia atual
        noticias_relacionadas = Noticia.objects.filter(
            categoria=noticia.categoria
        ).exclude(
            id=noticia.id
        ).select_related('categoria', 'autor').order_by('-data_publicacao')[:4]

    # Se não houver notícias relacionadas suficientes, buscar notícias gerais
    if len(noticias_relacionadas) < 4:
        noticias_gerais = Noticia.objects.exclude(
            id=noticia.id
        ).select_related('categoria', 'autor').order_by('-data_publicacao')[:4]

        # Combinar notícias relacionadas com gerais, evitando duplicatas
        ids_existentes = [n.id for n in noticias_relacionadas]
        for noticia_geral in noticias_gerais:
            if noticia_geral.id not in ids_existentes and len(noticias_relacionadas) < 4:
                noticias_relacionadas = list(noticias_relacionadas) + [noticia_geral]

    return render(request, 'detalhes_noticia.html', {
        'noticia': noticia,
        'noticia_salva': noticia_salva,
        'noticias_relacionadas': noticias_relacionadas,
        'enquete': enquete,
        'ja_votou_enquete': ja_votou_enquete
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


def painel_diario(request):
    """View para a página Painel Diário"""
    return render(request, 'painel_diario.html')


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


@require_http_methods(["POST"])
def enviar_feedback(request):
    """View para processar o envio de feedback"""
    try:
        # Verificar o Content-Type para decidir como processar
        content_type = request.content_type

        if content_type and 'application/json' in content_type:
            # Dados enviados via JSON
            try:
                data = json.loads(request.body)
                form = FeedbackForm(data)
            except json.JSONDecodeError:
                return JsonResponse({
                    'success': False,
                    'message': 'Erro ao processar os dados. Por favor, tente novamente.'
                }, status=400)
        else:
            # Dados enviados via FormData (multipart/form-data ou application/x-www-form-urlencoded)
            form = FeedbackForm(request.POST, request.FILES)

        if form.is_valid():
            feedback = form.save()
            return JsonResponse({
                'success': True,
                'message': 'Obrigado pelo seu feedback! Sua opinião é muito importante para nós.'
            })
        else:
            # Retorna os erros do formulário
            errors = {}
            for field, error_list in form.errors.items():
                errors[field] = error_list[0] if error_list else ''

            return JsonResponse({
                'success': False,
                'errors': errors,
                'message': 'Por favor, corrija os erros no formulário.'
            })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Erro ao enviar feedback: {str(e)}'
        }, status=500)


# ========== VIEWS DE ADMIN ==========

def is_staff(user):
    """Verifica se o usuário é staff/admin"""
    return user.is_authenticated and (user.is_staff or user.is_superuser)


@user_passes_test(is_staff, login_url='login_usuario')
def admin_dashboard(request):
    """View para o painel administrativo"""
    hoje = timezone.now().date()

    # Estatísticas
    total_noticias = Noticia.objects.count()
    total_categorias = Categoria.objects.count()
    total_autores = Autor.objects.count()
    visualizacoes_hoje = Visualizacao.objects.filter(data=hoje).count()

    # Listar todas as notícias
    noticias = Noticia.objects.select_related('categoria', 'autor').order_by('-data_publicacao')

    context = {
        'total_noticias': total_noticias,
        'total_categorias': total_categorias,
        'total_autores': total_autores,
        'visualizacoes_hoje': visualizacoes_hoje,
        'noticias': noticias,
    }

    return render(request, 'admin_dashboard.html', context)


@user_passes_test(is_staff, login_url='login_usuario')
def admin_criar_noticia(request):
    """View para criar uma nova notícia"""
    if request.method == 'POST':
        form = NoticiaForm(request.POST, request.FILES)
        if form.is_valid():
            noticia = form.save()

            # Processar enquete se existir
            tem_enquete = request.POST.get('tem_enquete') == 'on'
            if tem_enquete:
                titulo_enquete = request.POST.get('titulo_enquete', '').strip()
                pergunta_enquete = request.POST.get('pergunta_enquete', '').strip()

                if titulo_enquete and pergunta_enquete:
                    # Criar enquete
                    enquete = Enquete.objects.create(
                        titulo=titulo_enquete,
                        pergunta=pergunta_enquete,
                        noticia=noticia
                    )

                    # Criar opções
                    opcoes = request.POST.getlist('opcao[]')
                    for texto_opcao in opcoes:
                        texto_opcao = texto_opcao.strip()
                        if texto_opcao:
                            Opcao.objects.create(enquete=enquete, texto=texto_opcao)

            messages.success(request, f'Notícia "{noticia.titulo}" criada com sucesso!')
            return redirect('admin_dashboard')
    else:
        form = NoticiaForm()

    return render(request, 'admin_form_noticia.html', {'form': form})


@user_passes_test(is_staff, login_url='login_usuario')
def admin_editar_noticia(request, noticia_id):
    """View para editar uma notícia existente"""
    noticia = get_object_or_404(Noticia, id=noticia_id)

    if request.method == 'POST':
        form = NoticiaForm(request.POST, request.FILES, instance=noticia)
        if form.is_valid():
            noticia = form.save()

            # Processar enquete
            tem_enquete = request.POST.get('tem_enquete') == 'on'

            if tem_enquete:
                titulo_enquete = request.POST.get('titulo_enquete', '').strip()
                pergunta_enquete = request.POST.get('pergunta_enquete', '').strip()

                if titulo_enquete and pergunta_enquete:
                    # Atualizar ou criar enquete
                    if hasattr(noticia, 'enquete'):
                        enquete = noticia.enquete
                        enquete.titulo = titulo_enquete
                        enquete.pergunta = pergunta_enquete
                        enquete.save()
                        # Deletar opções antigas
                        enquete.opcoes.all().delete()
                    else:
                        enquete = Enquete.objects.create(
                            titulo=titulo_enquete,
                            pergunta=pergunta_enquete,
                            noticia=noticia
                        )

                    # Criar opções
                    opcoes = request.POST.getlist('opcao[]')
                    for texto_opcao in opcoes:
                        texto_opcao = texto_opcao.strip()
                        if texto_opcao:
                            Opcao.objects.create(enquete=enquete, texto=texto_opcao)
            else:
                # Se não tem enquete mas tinha antes, deletar
                if hasattr(noticia, 'enquete'):
                    noticia.enquete.delete()

            messages.success(request, f'Notícia "{noticia.titulo}" atualizada com sucesso!')
            return redirect('admin_dashboard')
    else:
        form = NoticiaForm(instance=noticia)

    return render(request, 'admin_form_noticia.html', {'form': form, 'noticia': noticia})


@user_passes_test(is_staff, login_url='login_usuario')
@require_http_methods(["POST"])
def admin_deletar_noticia(request, noticia_id):
    """View para deletar uma notícia"""
    noticia = get_object_or_404(Noticia, id=noticia_id)
    titulo = noticia.titulo
    noticia.delete()
    messages.success(request, f'Notícia "{titulo}" deletada com sucesso!')
    return redirect('admin_dashboard')


@user_passes_test(is_staff, login_url='login_usuario')
@require_http_methods(["POST"])
def admin_criar_autor(request):
    """View API para criar um novo autor via AJAX"""
    try:
        data = json.loads(request.body)
        nome = data.get('nome', '').strip()
        bio = data.get('bio', '').strip()
        
        if not nome:
            return JsonResponse({
                'success': False,
                'error': 'O nome do autor é obrigatório.'
            }, status=400)
        
        # Verificar se já existe um autor com esse nome
        if Autor.objects.filter(nome=nome).exists():
            return JsonResponse({
                'success': False,
                'error': 'Já existe um autor com esse nome.'
            }, status=400)
        
        # Criar o novo autor
        autor = Autor.objects.create(nome=nome, bio=bio)
        
        return JsonResponse({
            'success': True,
            'autor': {
                'id': autor.id,
                'nome': autor.nome
            },
            'message': f'Autor "{autor.nome}" criado com sucesso!'
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Erro ao processar dados.'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

