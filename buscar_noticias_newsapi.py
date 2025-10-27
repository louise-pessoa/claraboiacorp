"""
Busca notícias usando NewsAPI.org (fornece conteúdo completo)
Cadastre-se em: https://newsapi.org/ para obter uma API key gratuita
"""
import os
import django
import requests

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'claraboiacorp.settings')
django.setup()

from jcpemobile.models import Categoria, Autor, Noticia

# VOCÊ PRECISA SE CADASTRAR EM https://newsapi.org/ E COLOCAR SUA API KEY AQUI
NEWS_API_KEY = '5a2091aa5d434fe4905a933d047a9c7c'  # Cadastre-se gratuitamente em newsapi.org

class NewsAPIIntegration:
    """
    Integração com NewsAPI - Fornece conteúdo completo das notícias
    """
    BASE_URL = 'https://newsapi.org/v2'
    
    def __init__(self, api_key):
        self.api_key = api_key
        self.autor = self._get_or_create_autor()
    
    def _get_or_create_autor(self):
        autor, _ = Autor.objects.get_or_create(
            nome='NewsAPI',
            defaults={'bio': 'Notícias via NewsAPI.org'}
        )
        return autor
    
    def buscar_manchetes_brasil(self, categoria=None, limite=10):
        """
        Busca manchetes do Brasil
        Categorias: business, entertainment, general, health, science, sports, technology
        """
        url = f'{self.BASE_URL}/top-headlines'
        params = {
            'apiKey': self.api_key,
            'country': 'br',
            'pageSize': limite
        }
        
        if categoria:
            params['category'] = categoria
        
        return self._fazer_requisicao(url, params)
    
    def buscar_por_palavra_chave(self, palavra, idioma='pt', limite=10):
        """
        Busca notícias por palavra-chave
        """
        url = f'{self.BASE_URL}/everything'
        params = {
            'apiKey': self.api_key,
            'q': palavra,
            'language': idioma,
            'sortBy': 'publishedAt',
            'pageSize': limite
        }
        
        return self._fazer_requisicao(url, params)
    
    def _fazer_requisicao(self, url, params):
        """
        Faz a requisição para a API
        """
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get('status') == 'ok':
                return data.get('articles', [])
            else:
                print(f"Erro na API: {data.get('message')}")
                return []
        except Exception as e:
            print(f"Erro ao buscar notícias: {e}")
            return []
    
    def salvar_noticia(self, article, categoria=None):
        """
        Salva uma notícia no banco de dados
        """
        try:
            titulo = article.get('title', 'Sem título')
            
            # Remove sufixo do site (ex: " - CNN Brasil")
            if ' - ' in titulo:
                titulo = titulo.split(' - ')[0]
            
            # Verifica duplicata
            if Noticia.objects.filter(titulo=titulo).exists():
                return None
            
            # Extrai dados
            resumo = article.get('description', '')[:300]
            
            # CONTEÚDO COMPLETO vem da API! 🎉
            conteudo = article.get('content', '')
            
            # Se o conteúdo for muito curto, complementa com a descrição
            if len(conteudo) < 200:
                conteudo = resumo
            
            # Adiciona informações adicionais
            autor_artigo = article.get('author', 'Desconhecido')
            fonte = article.get('source', {}).get('name', 'Desconhecida')
            url = article.get('url', '')
            
            conteudo += f"\n\n---\nAutor: {autor_artigo}\nFonte: {fonte}\nLeia o original: {url}"
            
            # URL da imagem
            imagem_url = article.get('urlToImage')
            
            # Cria a notícia
            noticia = Noticia.objects.create(
                titulo=titulo,
                resumo=resumo,
                conteudo=conteudo,
                categoria=categoria,
                autor=self.autor
            )
            
            # TODO: Baixar e salvar a imagem se desejar
            # if imagem_url:
            #     # código para baixar e salvar imagem
            
            print(f"✓ {titulo}")
            return noticia
            
        except Exception as e:
            print(f"✗ Erro ao salvar: {e}")
            return None


def buscar_noticias_newsapi():
    """
    Função principal
    """
    if NEWS_API_KEY == 'SUA_API_KEY_AQUI':
        print("❌ ERRO: Configure sua API Key do NewsAPI!")
        print("1. Acesse: https://newsapi.org/")
        print("2. Crie uma conta gratuita")
        print("3. Copie sua API Key")
        print("4. Cole no arquivo buscar_noticias_newsapi.py")
        return
    
    newsapi = NewsAPIIntegration(NEWS_API_KEY)
    
    # Mapeia categorias
    categorias_map = {
        'business': 'Economia',
        'entertainment': 'Cultura',
        'general': 'Geral',
        'health': 'Saúde',
        'science': 'Ciência',
        'sports': 'Esportes',
        'technology': 'Tecnologia'
    }
    
    total = 0
    
    print("\n=== BUSCANDO NOTÍCIAS DO BRASIL ===\n")
    
    # Busca por categoria
    for cat_api, cat_nome in categorias_map.items():
        print(f"--- {cat_nome} ---")
        categoria = Categoria.objects.get_or_create(nome=cat_nome)[0]
        articles = newsapi.buscar_manchetes_brasil(categoria=cat_api, limite=5)
        
        for article in articles:
            noticia = newsapi.salvar_noticia(article, categoria)
            if noticia:
                total += 1
    
    # Busca específica de Pernambuco
    print(f"\n--- Pernambuco ---")
    categoria_pe = Categoria.objects.get_or_create(nome='Pernambuco')[0]
    articles = newsapi.buscar_por_palavra_chave('Pernambuco OR Recife', limite=5)
    
    for article in articles:
        noticia = newsapi.salvar_noticia(article, categoria_pe)
        if noticia:
            total += 1
    
    print(f"\n✅ Total de notícias salvas: {total}")


if __name__ == '__main__':
    buscar_noticias_newsapi()
