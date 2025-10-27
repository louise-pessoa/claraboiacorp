# jcpemobile/management/commands/buscar_noticias_newsapi.py
from django.core.management.base import BaseCommand
import requests
import os
from jcpemobile.models import Categoria, Autor, Noticia


class Command(BaseCommand):
    help = 'Busca notícias via NewsAPI.org (fornece conteúdo completo)'

    def add_arguments(self, parser):
        parser.add_argument('--api-key', type=str, help='Sua API Key do NewsAPI (ou configure no .env)')
        parser.add_argument('--categoria', type=str, help='Categoria específica')
        parser.add_argument('--limite', type=int, default=5, help='Limite por categoria')

    def handle(self, *args, **options):
        # Tenta pegar a API key do argumento ou variável de ambiente
        api_key = options.get('api_key') or os.getenv('NEWS_API_KEY')
        
        if not api_key:
            self.stdout.write(self.style.ERROR('\n❌ API Key não configurada!\n'))
            self.stdout.write('Opções para configurar:\n')
            self.stdout.write('1. Use: python manage.py buscar_noticias_newsapi --api-key SUA_KEY\n')
            self.stdout.write('2. Ou adicione NEWS_API_KEY=sua_key no arquivo .env\n')
            self.stdout.write('\n📝 Como obter sua API Key GRATUITA:')
            self.stdout.write('   1. Acesse: https://newsapi.org/')
            self.stdout.write('   2. Clique em "Get API Key"')
            self.stdout.write('   3. Preencha o formulário (é grátis)')
            self.stdout.write('   4. Copie sua API Key')
            self.stdout.write('   5. Use no comando acima\n')
            return
        
        limite = options['limite']
        categoria_especifica = options.get('categoria')
        
        self.stdout.write(self.style.SUCCESS('Buscando notícias via NewsAPI...\n'))
        
        # Cria autor
        autor, _ = Autor.objects.get_or_create(
            nome='NewsAPI',
            defaults={'bio': 'Notícias via NewsAPI.org'}
        )
        
        categorias_map = {
            'Economia': 'economia brasil',
            'Esportes': 'esportes brasil OR futebol brasil',
            'Tecnologia': 'tecnologia brasil',
            'Política': 'política brasil',
            'Cultura': 'cultura brasil',
            'Geral': 'brasil',
            'Pernambuco': 'Pernambuco OR Recife'
        }
        
        total = 0
        
        if categoria_especifica:
            # Busca apenas uma categoria
            self.stdout.write(f'\n--- {categoria_especifica} ---')
            palavra = categorias_map.get(categoria_especifica, categoria_especifica)
            total = self._buscar_por_palavra(api_key, palavra, limite, autor, categoria_especifica)
        else:
            # Busca todas as categorias usando palavras-chave
            for cat_nome, palavra in categorias_map.items():
                self.stdout.write(f'\n--- {cat_nome} ---')
                total += self._buscar_por_palavra(api_key, palavra, limite, autor, cat_nome)
        
        self.stdout.write(self.style.SUCCESS(f'\n✅ Total: {total} notícias salvas'))
    
    def _buscar_categoria(self, api_key, cat_api, limite, autor, cat_nome=None):
        """Busca notícias de uma categoria"""
        if not cat_nome:
            cat_nome = cat_api
        
        categoria, _ = Categoria.objects.get_or_create(nome=cat_nome)
        
        url = 'https://newsapi.org/v2/top-headlines'
        params = {
            'apiKey': api_key,
            'country': 'br',
            'category': cat_api if cat_api in ['business', 'sports', 'technology', 'entertainment', 'general'] else None,
            'pageSize': limite
        }
        
        if not params['category']:
            del params['category']
        
        return self._processar_requisicao(url, params, categoria, autor)
    
    def _buscar_por_palavra(self, api_key, palavra, limite, autor, cat_nome):
        """Busca notícias por palavra-chave"""
        categoria, _ = Categoria.objects.get_or_create(nome=cat_nome)
        
        url = 'https://newsapi.org/v2/everything'
        params = {
            'apiKey': api_key,
            'q': palavra,
            'language': 'pt',
            'sortBy': 'publishedAt',
            'pageSize': limite
        }
        
        return self._processar_requisicao(url, params, categoria, autor)
    
    def _processar_requisicao(self, url, params, categoria, autor):
        """Processa a requisição e salva as notícias"""
        contador = 0
        
        try:
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            # Debug
            self.stdout.write(f'   Status: {data.get("status")}')
            self.stdout.write(f'   Total de artigos: {data.get("totalResults", 0)}')
            
            if data.get('status') == 'ok':
                articles = data.get('articles', [])
                
                if not articles:
                    self.stdout.write(self.style.WARNING('   ⚠ Nenhum artigo retornado'))
                
                for article in articles:
                    titulo = article.get('title', '')
                    
                    if not titulo:
                        continue
                    
                    # Remove sufixo do site
                    if ' - ' in titulo:
                        titulo = titulo.split(' - ')[0]
                    
                    if Noticia.objects.filter(titulo=titulo).exists():
                        continue
                    
                    resumo = article.get('description', '') or ''
                    if resumo:
                        resumo = resumo[:300]
                    
                    # CONTEÚDO COMPLETO da API
                    conteudo = article.get('content', '') or ''
                    
                    # Remove o sufixo "+xxx chars" do NewsAPI
                    import re
                    conteudo = re.sub(r'\s*\[\+\d+\s+chars?\]$', '', conteudo)
                    
                    # Tenta fazer scraping do conteúdo completo
                    url_original = article.get('url', '')
                    conteudo_completo = self._extrair_conteudo_completo(url_original)
                    
                    # Usa o conteúdo extraído se for melhor que o da API
                    if conteudo_completo and len(conteudo_completo) > len(conteudo):
                        conteudo = conteudo_completo
                    elif not conteudo or len(conteudo) < 100:
                        # Se não tem conteúdo bom, usa o resumo
                        conteudo = resumo if resumo else "Conteúdo não disponível."
                    
                    # VERIFICA SE O CONTEÚDO É LONGO O SUFICIENTE
                    # Rejeita notícias com conteúdo muito curto (scraping falhou)
                    if len(conteudo) < 800:
                        continue  # Pula para próxima notícia
                    
                    # Adiciona informações da fonte
                    autor_artigo = article.get('author') or 'Desconhecido'
                    fonte = article.get('source', {}).get('name') or 'Desconhecida'
                    
                    conteudo += f"\n\n---\nAutor: {autor_artigo}\nFonte: {fonte}\nLeia o artigo completo: {url_original}"
                    
                    # Baixa a imagem ANTES de criar a notícia
                    imagem_url = article.get('urlToImage')
                    if not imagem_url:
                        continue  # Pula notícias sem URL de imagem
                    
                    # Cria a notícia
                    noticia = Noticia.objects.create(
                        titulo=titulo,
                        resumo=resumo,
                        conteudo=conteudo,
                        categoria=categoria,
                        autor=autor
                    )
                    
                    # Tenta baixar a imagem
                    imagem_salva = self._baixar_imagem(noticia, imagem_url)
                    
                    if not imagem_salva:
                        # Se não conseguiu baixar a imagem, deleta a notícia
                        noticia.delete()
                        continue
                    
                    self.stdout.write(self.style.SUCCESS(f'✓ {titulo[:60]}...'))
                    contador += 1
            else:
                erro = data.get('message', 'Erro desconhecido')
                self.stderr.write(f'❌ Erro da API: {erro}')
                
        except Exception as e:
            self.stderr.write(f'❌ Erro: {e}')
        
        return contador
    
    def _baixar_imagem(self, noticia, imagem_url):
        """Baixa e salva a imagem da notícia. Retorna True se sucesso, False se falhar."""
        try:
            import os
            from django.core.files.base import ContentFile
            
            response = requests.get(imagem_url, timeout=10)
            response.raise_for_status()
            
            # Extrai extensão da URL
            ext = imagem_url.split('.')[-1].split('?')[0][:4]
            if ext not in ['jpg', 'jpeg', 'png', 'webp']:
                ext = 'jpg'
            
            # Nome do arquivo (sem duplicar 'noticias/')
            nome_arquivo = f'newsapi_{noticia.id}.{ext}'
            
            # Salva a imagem
            noticia.imagem.save(
                nome_arquivo,
                ContentFile(response.content),
                save=True
            )
            
            return True
            
        except Exception as e:
            return False
    
    def _extrair_conteudo_completo(self, url):
        """Extrai o conteúdo completo do artigo fazendo scraping"""
        try:
            from bs4 import BeautifulSoup
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove elementos indesejados
            for elemento in soup(['script', 'style', 'nav', 'header', 'footer', 'aside', 'iframe', 'form', 'button']):
                elemento.decompose()
            
            # Tenta encontrar o conteúdo principal com seletores mais específicos
            conteudo = None
            selectors = [
                # Sites brasileiros populares
                '.mc-article-body',  # Metropoles
                '.content-text',
                '.article-body',
                '.post-content',
                '.entry-content',
                '[itemprop="articleBody"]',
                'article p',
                # Seletores genéricos
                'article',
                '[class*="article-content"]',
                '[class*="post-body"]',
                '[class*="story-body"]',
                '[class*="texto"]',
                '[class*="materia"]',
                'main article',
                'main'
            ]
            
            for selector in selectors:
                elemento = soup.select_one(selector)
                if elemento:
                    # Se encontrou apenas 'article', pega todos os parágrafos
                    if selector in ['article', 'main article', 'main']:
                        paragrafos = elemento.find_all('p')
                    else:
                        conteudo = elemento
                        break
                    
                    if paragrafos and len(paragrafos) > 2:
                        conteudo = elemento
                        break
            
            if conteudo:
                # Extrai parágrafos
                paragrafos = conteudo.find_all('p')
                textos = []
                
                for p in paragrafos:
                    texto = p.get_text().strip()
                    # Ignora parágrafos muito curtos, vazios ou com apenas links
                    if len(texto) > 40 and not texto.startswith('Leia também'):
                        textos.append(texto)
                
                conteudo_final = '\n\n'.join(textos)
                
                # Remove espaços extras
                import re
                conteudo_final = re.sub(r'\n\n+', '\n\n', conteudo_final)
                conteudo_final = re.sub(r' +', ' ', conteudo_final)
                
                # Limita o tamanho
                if len(conteudo_final) > 8000:
                    conteudo_final = conteudo_final[:8000] + '...'
                
                return conteudo_final if len(conteudo_final) > 300 else ''
            
            return ''
            
        except Exception as e:
            return ''
