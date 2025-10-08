from django.contrib import admin
from .models import Categoria, Tag, Noticia, Autor


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
