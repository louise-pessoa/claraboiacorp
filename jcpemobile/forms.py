from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Noticia, Categoria, Autor, Tag
import re

class CadastroUsuarioForm(forms.ModelForm):
    """Formulário de cadastro de novo usuário"""
    
    nome = forms.CharField(
        max_length=150,
        required=True,
        error_messages={
            'required': 'O nome é obrigatório.',
            'max_length': 'O nome deve ter no máximo 150 caracteres.'
        }
    )
    
    email = forms.EmailField(
        required=True,
        error_messages={
            'required': 'O e-mail é obrigatório.',
            'invalid': 'Digite um e-mail válido.'
        }
    )
    
    senha = forms.CharField(
        min_length=8,
        required=True,
        error_messages={
            'required': 'A senha é obrigatória.',
            'min_length': 'A senha deve ter no mínimo 8 caracteres.'
        }
    )
    
    confirmar_senha = forms.CharField(
        required=True,
        error_messages={
            'required': 'A confirmação de senha é obrigatória.'
        }
    )
    
    class Meta:
        model = User
        fields = ['nome', 'email', 'senha']
    
    def clean_email(self):
        """Valida se o e-mail já está cadastrado"""
        email = self.cleaned_data.get('email')
        
        if email:
            # Verifica formato do e-mail
            email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_regex, email):
                raise ValidationError('Digite um e-mail válido.')
            
            # Verifica se e-mail já existe
            if User.objects.filter(email=email).exists():
                raise ValidationError('E-mail já registrado.')
        
        return email
    
    def clean_senha(self):
        """Valida o tamanho mínimo da senha"""
        senha = self.cleaned_data.get('senha')
        
        if senha and len(senha) < 8:
            raise ValidationError('A senha deve ter no mínimo 8 caracteres.')
        
        return senha
    
    def clean(self):
        """Valida se as senhas coincidem"""
        cleaned_data = super().clean()
        senha = cleaned_data.get('senha')
        confirmar_senha = cleaned_data.get('confirmar_senha')
        
        if senha and confirmar_senha and senha != confirmar_senha:
            raise ValidationError({'confirmar_senha': 'As senhas não coincidem.'})
        
        return cleaned_data
    
    def save(self, commit=True):
        """Cria o usuário com os dados validados"""
        user = User.objects.create_user(
            username=self.cleaned_data['email'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['senha'],
            first_name=self.cleaned_data['nome']
        )
        return user


class NoticiaForm(forms.ModelForm):
    """Formulário para criar e editar notícias com editor rico"""

    class Meta:
        model = Noticia
        fields = ['titulo', 'resumo', 'conteudo', 'imagem', 'categoria', 'autor', 'tags']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control editor-titulo',
                'placeholder': 'Digite o título da notícia',
                'id': 'id_titulo'
            }),
            'resumo': forms.Textarea(attrs={
                'class': 'form-control editor-resumo',
                'rows': 3,
                'placeholder': 'Breve resumo da notícia (máx. 300 caracteres)',
                'id': 'id_resumo'
            }),
            'conteudo': forms.Textarea(attrs={
                'class': 'form-control editor-conteudo-hidden',
                'rows': 10,
                'id': 'id_conteudo',
                'style': 'display: none;'
            }),
            'imagem': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
                'id': 'id_imagem_principal'
            }),
            'categoria': forms.Select(attrs={
                'class': 'form-control',
                'id': 'id_categoria'
            }),
            'autor': forms.Select(attrs={
                'class': 'form-control',
                'id': 'id_autor'
            }),
            'tags': forms.SelectMultiple(attrs={
                'class': 'form-control',
                'id': 'id_tags'
            }),
        }
        labels = {
            'titulo': 'Título',
            'resumo': 'Resumo',
            'conteudo': 'Conteúdo',
            'imagem': 'Imagem Principal',
            'categoria': 'Categoria',
            'autor': 'Autor',
            'tags': 'Tags',
        }
        help_texts = {
            'resumo': 'Máximo de 300 caracteres',
            'tags': 'Mantenha pressionado "Control" ou "Command" para selecionar mais de uma',
            'conteudo': 'Use o editor abaixo para formatar seu conteúdo',
        }

    def clean_titulo(self):
        titulo = self.cleaned_data.get('titulo')
        if len(titulo) < 10:
            raise ValidationError('O título deve ter pelo menos 10 caracteres.')
        return titulo

    def clean_resumo(self):
        resumo = self.cleaned_data.get('resumo')
        if resumo and len(resumo) > 300:
            raise ValidationError('O resumo não pode ter mais de 300 caracteres.')
        return resumo


class CategoriaForm(forms.ModelForm):
    """Formulário para criar e editar categorias"""

    class Meta:
        model = Categoria
        fields = ['nome']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome da categoria'
            })
        }


class AutorForm(forms.ModelForm):
    """Formulário para criar e editar autores"""

    class Meta:
        model = Autor
        fields = ['nome', 'bio', 'foto']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome do autor'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Biografia do autor'
            }),
            'foto': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }
