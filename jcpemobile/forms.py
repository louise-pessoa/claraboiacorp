from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
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
