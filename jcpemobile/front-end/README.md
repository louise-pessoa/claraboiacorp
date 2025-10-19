# Front-end - Jornal do Commercio

## 📁 Estrutura de Arquivos

```
front-end/
├── html/
│   ├── index.html              # Página principal
│   └── detalhes_noticia.html   # Página de detalhes da notícia
├── css/
│   ├── reset.css               # Reset CSS
│   ├── variaveis.css           # Variáveis CSS (Design System)
│   ├── base.css                # Estilos base e tipografia
│   ├── componentes.css         # Componentes reutilizáveis
│   ├── layout.css              # Layout geral (header, menu, footer)
│   ├── home-layout.css         # Layout específico da home
│   ├── detalhes-noticia.css    # Layout da página de detalhes
│   └── responsivo.css          # Media queries e responsividade
├── js/
│   ├── app.js                  # Inicialização e controle principal
│   ├── navegacao.js            # Menu lateral e navegação
│   ├── busca.js                # Sistema de busca e filtros
│   ├── noticias.js             # Gerenciamento de notícias
│   └── toggle-versao.js        # Toggle versão curta/completa
├── images/
│   └── logo-jc.png             # Logo do Jornal do Commercio
└── README.md                   # Este arquivo
```

## 🎯 Tecnologias Utilizadas

- **HTML5**: Estrutura semântica
- **CSS3**: Flexbox, Grid, Variáveis CSS, Animações
- **JavaScript Vanilla**: Sem frameworks ou bibliotecas
- **Font Awesome 6.4.0**: Ícones
- **Google Fonts**: Tipografia (Inter)

## 🚀 Como Usar (Standalone)

### Opção 1: Abrir diretamente
```bash
# Navegue até a pasta html/
cd front-end/html/
# Abra o index.html no navegador
```

### Opção 2: Servidor local
```bash
# Python
python -m http.server 8000

# Node.js
npx http-server -p 8000

# VS Code Live Server
# Instale a extensão e clique com botão direito em index.html
```

## 🔗 Integração com Django

### Passo 1: Estrutura Django Recomendada

Mova os arquivos para a estrutura Django padrão:

```
seu_projeto_django/
├── jcpemobile/                    # App principal
│   ├── static/jcpemobile/
│   │   ├── css/                   # Copiar front-end/css/
│   │   ├── js/                    # Copiar front-end/js/
│   │   └── images/                # Copiar front-end/images/
│   ├── templates/jcpemobile/
│   │   ├── base.html              # Template base
│   │   ├── index.html             # Converter de front-end/html/
│   │   └── detalhes_noticia.html  # Converter de front-end/html/
│   ├── views.py
│   ├── urls.py
│   └── models.py
└── manage.py
```

### Passo 2: Converter HTML para Templates Django

**Antes (HTML estático):**
```html
<link rel="stylesheet" href="css/reset.css">
<script src="js/app.js"></script>
<img src="images/logo-jc.png" alt="Logo">
```

**Depois (Template Django):**
```django
{% load static %}

<link rel="stylesheet" href="{% static 'jcpemobile/css/reset.css' %}">
<script src="{% static 'jcpemobile/js/app.js' %}"></script>
<img src="{% static 'jcpemobile/images/logo-jc.png' %}" alt="Logo">
```

### Passo 3: Criar Template Base

Crie um `templates/jcpemobile/base.html`:

```django
{% load static %}
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>{% block title %}Jornal do Commercio{% endblock %}</title>

    <!-- Fontes -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">

    <!-- CSS -->
    <link rel="stylesheet" href="{% static 'jcpemobile/css/reset.css' %}">
    <link rel="stylesheet" href="{% static 'jcpemobile/css/variaveis.css' %}">
    <link rel="stylesheet" href="{% static 'jcpemobile/css/base.css' %}">
    <link rel="stylesheet" href="{% static 'jcpemobile/css/componentes.css' %}">
    <link rel="stylesheet" href="{% static 'jcpemobile/css/layout.css' %}">
    {% block extra_css %}{% endblock %}
    <link rel="stylesheet" href="{% static 'jcpemobile/css/responsivo.css' %}">

    <!-- Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body>
    <div class="top-bar"></div>

    {% include 'jcpemobile/partials/header.html' %}
    {% include 'jcpemobile/partials/menu_lateral.html' %}

    <main class="conteudo-principal" id="conteudoPrincipal">
        {% block content %}{% endblock %}
    </main>

    {% include 'jcpemobile/partials/navegacao_inferior.html' %}
    {% include 'jcpemobile/partials/footer.html' %}

    <!-- JavaScript -->
    <script src="{% static 'jcpemobile/js/app.js' %}"></script>
    <script src="{% static 'jcpemobile/js/navegacao.js' %}"></script>
    <script src="{% static 'jcpemobile/js/busca.js' %}"></script>
    {% block extra_js %}{% endblock %}
</body>
</html>
```

### Passo 4: Criar Views e URLs

**views.py:**
```python
from django.shortcuts import render, get_object_or_404
from .models import Noticia

def index(request):
    noticias = Noticia.objects.filter(publicada=True).order_by('-data_publicacao')
    context = {
        'noticias': noticias
    }
    return render(request, 'jcpemobile/index.html', context)

def detalhes_noticia(request, slug):
    noticia = get_object_or_404(Noticia, slug=slug, publicada=True)
    noticias_relacionadas = Noticia.objects.filter(
        categoria=noticia.categoria
    ).exclude(id=noticia.id)[:3]

    context = {
        'noticia': noticia,
        'noticias_relacionadas': noticias_relacionadas
    }
    return render(request, 'jcpemobile/detalhes_noticia.html', context)
```

**urls.py:**
```python
from django.urls import path
from . import views

app_name = 'jcpemobile'

urlpatterns = [
    path('', views.index, name='index'),
    path('noticia/<slug:slug>/', views.detalhes_noticia, name='detalhes_noticia'),
]
```

### Passo 5: Configurar Settings

**settings.py:**
```python
# Adicionar o app
INSTALLED_APPS = [
    # ...
    'jcpemobile',
]

# Configurar static files
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'jcpemobile/static',
]
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media files (para uploads de imagens)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

## 📝 Alterações Necessárias nos Arquivos

### 1. Atualizar Caminhos de Imagens

Nos arquivos HTML, todas as referências a imagens devem ser atualizadas:

```html
<!-- Antes -->
<img src="components/1_logo_jc-27530572.png">

<!-- Depois -->
{% load static %}
<img src="{% static 'jcpemobile/images/logo-jc.png' %}">
```

### 2. Atualizar Links entre Páginas

```html
<!-- Antes -->
<a href="detalhes_noticia.html">

<!-- Depois -->
<a href="{% url 'jcpemobile:detalhes_noticia' slug=noticia.slug %}">
```

### 3. Dados Dinâmicos

Substituir conteúdo estático por dados do banco:

```html
<!-- Antes (estático) -->
<h1>Recife anuncia novo plano de mobilidade urbana para 2025</h1>

<!-- Depois (dinâmico) -->
<h1>{{ noticia.titulo }}</h1>
```

## 🔧 Comandos Django Úteis

```bash
# Coletar arquivos estáticos
python manage.py collectstatic

# Criar migrações
python manage.py makemigrations

# Aplicar migrações
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser

# Rodar servidor de desenvolvimento
python manage.py runserver
```

## 📦 Dependências Sugeridas

Crie um `requirements.txt`:

```txt
Django>=4.2,<5.0
Pillow>=10.0.0              # Para manipulação de imagens
django-ckeditor>=6.7.0      # Editor WYSIWYG para conteúdo
django-taggit>=5.0.0        # Sistema de tags
python-slugify>=8.0.0       # Geração de slugs
```

## 🎨 Customizações para Django

### 1. Filtros de Template Customizados

Crie `jcpemobile/templatetags/jc_filters.py`:

```python
from django import template
from datetime import datetime

register = template.Library()

@register.filter
def tempo_relativo(data):
    """Retorna tempo relativo (Há X horas)"""
    agora = datetime.now()
    diferenca = agora - data

    minutos = diferenca.total_seconds() / 60
    if minutos < 60:
        return f"Há {int(minutos)} minutos"

    horas = minutos / 60
    if horas < 24:
        return f"Há {int(horas)} horas"

    dias = horas / 24
    return f"Há {int(dias)} dias"
```

### 2. Context Processors

Adicione em `settings.py`:

```python
TEMPLATES = [
    {
        'OPTIONS': {
            'context_processors': [
                # ...
                'jcpemobile.context_processors.categorias_menu',
            ],
        },
    },
]
```

Crie `jcpemobile/context_processors.py`:

```python
from .models import Categoria

def categorias_menu(request):
    """Disponibiliza categorias em todos os templates"""
    return {
        'categorias': Categoria.objects.all()
    }
```

## 📱 Próximos Passos

1. ✅ Criar models para Noticia, Categoria, Autor
2. ✅ Configurar Django Admin
3. ✅ Implementar API REST (Django REST Framework)
4. ✅ Adicionar sistema de busca (django-haystack ou Elasticsearch)
5. ✅ Implementar cache (Redis)
6. ✅ Configurar deploy (Gunicorn, Nginx)

## 📚 Recursos Úteis

- [Documentação Django](https://docs.djangoproject.com/)
- [Django Static Files](https://docs.djangoproject.com/en/stable/howto/static-files/)
- [Django Templates](https://docs.djangoproject.com/en/stable/topics/templates/)

## 🐛 Troubleshooting

### Arquivos estáticos não carregam
```bash
# Verificar STATIC_URL e STATICFILES_DIRS
# Rodar collectstatic
python manage.py collectstatic --noinput
```

### Imagens não aparecem
```bash
# Verificar MEDIA_URL e MEDIA_ROOT
# Adicionar em urls.py principal:
from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

---

**Desenvolvido para Jornal do Commercio**
Protótipo Front-end - Janeiro 2025
