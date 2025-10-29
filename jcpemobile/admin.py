from django.contrib import admin
from .models import Categoria, Tag, Noticia, Autor, Feedback


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
	list_display = ('nome', 'slug')
	search_fields = ('nome',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
	list_display = ('nome',)
	search_fields = ('nome',)


@admin.register(Noticia)
class NoticiaAdmin(admin.ModelAdmin):
	list_display = ('titulo', 'categoria', 'autor', 'data_publicacao')
	search_fields = ('titulo', 'resumo', 'conteudo')
	list_filter = ('categoria', 'autor', 'tags')


@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
	list_display = ('nome',)
	search_fields = ('nome',)


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
	list_display = ('nome', 'email', 'avaliacao', 'data_envio', 'respondido')
	search_fields = ('nome', 'email', 'comentario')
	list_filter = ('avaliacao', 'respondido', 'data_envio')
	readonly_fields = ('data_envio',)
	list_editable = ('respondido',)
