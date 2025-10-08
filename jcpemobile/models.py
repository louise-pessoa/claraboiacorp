from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

class Categoria(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome

class Tag(models.Model):
    nome = models.CharField(max_length=50, unique=True)
    # tag de mais acessadas , geolocalização 

    def __str__(self):
        return self.nome

class Noticia(models.Model):
    titulo = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    resumo = models.TextField(max_length=300, blank=True, null=True)
    conteudo = models.TextField()
    imagem = models.ImageField(upload_to="noticias/", blank=True, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, related_name="noticias")
    autor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="noticias")
    tags = models.ManyToManyField(Tag, blank=True, related_name="noticias")
    data_publicacao = models.DateTimeField(auto_now_add=True)
    # atualizado_em = models.DateTimeField(auto_now=True) se houve uma atulização vc "perde" a data original de publicação

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titulo

class Autor(models.Model):
    nome = models.CharField(max_length=100)
    bio = models.TextField(blank=True, null=True)
    foto = models.ImageField(upload_to="autores/", blank=True, null=True)

    def __str__(self):
        return self.nome
class Visualizacao(models.Model):
    noticia = models.ForeignKey(Noticia, on_delete=models.CASCADE, related_name="visualizacoes")
    ip_usuario = models.GenericIPAddressField()
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Visualização em {self.noticia.titulo} ({self.data})"

class Contato(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    assunto = models.CharField(max_length=150)
    mensagem = models.TextField()
    data_envio = models.DateTimeField(auto_now_add=True)
    lido = models.BooleanField(default=False)

    def __str__(self):
        return f"Mensagem de {self.nome} - {self.assunto}"
