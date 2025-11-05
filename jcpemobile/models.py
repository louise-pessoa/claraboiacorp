# jcpemobile/models.py
from django.db import models
from django.utils.text import slugify
from django.utils import timezone
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
    
class Autor(models.Model):
    nome = models.CharField(max_length=100)
    bio = models.TextField(blank=True, null=True)
    foto = models.ImageField(upload_to="autores/", blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome

class Tag(models.Model):
    nome = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nome

class Noticia(models.Model):
    titulo = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    resumo = models.TextField(max_length=300, blank=True, null=True)
    conteudo = models.TextField()
    imagem = models.ImageField(upload_to="noticias/", blank=True, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, related_name="noticias")
    autor = models.ForeignKey(Autor, on_delete=models.SET_NULL, null=True, related_name="noticias")
    tags = models.ManyToManyField(Tag, blank=True, related_name="noticias")
    data_publicacao = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)
        super().save(*args, **kwargs)

    def visualizacoes_do_dia(self):
        # Conta visualizações únicas (por IP) do dia atual
        hoje = timezone.now().date()
        return self.visualizacoes.filter(data=hoje).values('ip_address').distinct().count()

    def total_visualizacoes(self):
        return self.visualizacoes.count()

    def __str__(self):
        return self.titulo

class Visualizacao(models.Model):
    noticia = models.ForeignKey(Noticia, on_delete=models.CASCADE, related_name="visualizacoes")
    ip_address = models.GenericIPAddressField()  # Renamed from ip_usuario
    data_visualizacao = models.DateTimeField(auto_now_add=True)  # For precise timestamp
    data = models.DateField(null=True, blank=True)  # For daily view counting

    class Meta:
        unique_together = ('noticia', 'ip_address', 'data')
        indexes = [
            models.Index(fields=['data']),
        ]

    def __str__(self):
        return f"Visualização em {self.noticia.titulo} ({self.data})"

class Feedback(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    avaliacao = models.IntegerField(
        choices=[
            (1, 'Ruim'),
            (2, 'Regular'),
            (3, 'Bom'),
            (4, 'Muito bom'),
            (5, 'Excelente'),
        ]
    )
    comentario = models.TextField(blank=True, null=True)
    imagem = models.ImageField(upload_to='feedbacks/', blank=True, null=True)
    data_envio = models.DateTimeField(auto_now_add=True)
    respondido = models.BooleanField(default=False)

    def __str__(self):
        return f"Feedback de {self.nome} - {self.get_avaliacao_display()}"

class NoticaSalva(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="noticias_salvas")
    noticia = models.ForeignKey(Noticia, on_delete=models.CASCADE, related_name="salvamentos")
    data_salvamento = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'noticia')
        ordering = ['-data_salvamento']

    def __str__(self):
        return f"{self.usuario.username} salvou {self.noticia.titulo}"

class Enquete(models.Model):
    titulo = models.CharField(max_length=255)
    pergunta = models.CharField(max_length=255)

    def __str__(self):
        return self.titulo

    def total_votos(self):
        return sum(opcao.votos.count() for opcao in self.opcoes.all())


class Opcao(models.Model):
    enquete = models.ForeignKey(Enquete, on_delete=models.CASCADE, related_name="opcoes")
    texto = models.CharField(max_length=200)

    def __str__(self):
        return self.texto

    def percentual(self):
        total = self.enquete.total_votos()
        return (self.votos.count() / total * 100) if total > 0 else 0


class Voto(models.Model):
    opcao = models.ForeignKey(Opcao, on_delete=models.CASCADE, related_name="votos")
    ip_usuario = models.GenericIPAddressField()
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Voto em {self.opcao.texto} ({self.ip_usuario})"
