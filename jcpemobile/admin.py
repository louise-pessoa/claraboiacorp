from django.contrib import admin
from .models import Categoria, Tag, Noticia, Autor, Feedback, Enquete, Opcao, Voto

# Mostra as opções dentro da página de edição de uma enquete
class OpcaoInline(admin.TabularInline):
    model = Opcao
    extra = 2  # quantas opções aparecem por padrão para adicionar
    min_num = 2  # exige no mínimo 2 opções (pode remover se quiser)
    can_delete = True  # permite remover opções

# Admin principal da Enquete
@admin.register(Enquete)
class EnqueteAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'pergunta', 'total_votos')
    search_fields = ('titulo', 'pergunta')
    inlines = [OpcaoInline]  # mostra as opções na mesma tela da enquete

# Admin para visualizar os votos (só leitura)
@admin.register(Voto)
class VotoAdmin(admin.ModelAdmin):
    list_display = ('opcao', 'ip_usuario', 'data')
    list_filter = ('data',)
    search_fields = ('ip_usuario', 'opcao__texto', 'opcao__enquete__titulo')
    readonly_fields = ('opcao', 'ip_usuario', 'data')  # impede alterar votos

    def has_add_permission(self, request):
        return False  # impede adicionar votos manualmente

    def has_change_permission(self, request, obj=None):
        return False  # impede editar votos

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
