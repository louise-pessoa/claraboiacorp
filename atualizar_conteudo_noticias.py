#!/usr/bin/env python
"""
Script para re-scrapar notícias existentes e atualizar o conteúdo
"""
import os
import django
import re

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'claraboiacorp.settings')
django.setup()

from jcpemobile.models import Noticia
import requests
from bs4 import BeautifulSoup

def extrair_url_do_rodape(conteudo):
    """Extrai a URL do rodapé da notícia"""
    match = re.search(r'Leia o artigo completo: (https?://[^\s]+)', conteudo)
    return match.group(1) if match else None

def extrair_conteudo_completo(url):
    """Extrai o conteúdo completo do artigo fazendo scraping"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove elementos indesejados
        for elemento in soup(['script', 'style', 'nav', 'header', 'footer', 'aside', 'iframe', 'form', 'button']):
            elemento.decompose()
        
        # Seletores específicos para sites brasileiros
        selectors = [
            '.mc-article-body',  # Metropoles
            '.content-text',
            '.article-body',
            '.post-content',
            '.entry-content',
            '[itemprop="articleBody"]',
            'article p',
            'article',
            '[class*="article-content"]',
            '[class*="post-body"]',
            '[class*="story-body"]',
            '[class*="texto"]',
            '[class*="materia"]',
            'main article',
            'main'
        ]
        
        conteudo = None
        for selector in selectors:
            elemento = soup.select_one(selector)
            if elemento:
                if selector in ['article', 'main article', 'main']:
                    paragrafos = elemento.find_all('p')
                else:
                    conteudo = elemento
                    break
                
                if paragrafos and len(paragrafos) > 2:
                    conteudo = elemento
                    break
        
        if conteudo:
            paragrafos = conteudo.find_all('p')
            textos = []
            
            for p in paragrafos:
                texto = p.get_text().strip()
                if len(texto) > 40 and not texto.startswith('Leia também'):
                    textos.append(texto)
            
            conteudo_final = '\n\n'.join(textos)
            
            # Limpa espaços extras
            conteudo_final = re.sub(r'\n\n+', '\n\n', conteudo_final)
            conteudo_final = re.sub(r' +', ' ', conteudo_final)
            
            if len(conteudo_final) > 8000:
                conteudo_final = conteudo_final[:8000] + '...'
            
            return conteudo_final if len(conteudo_final) > 300 else None
        
        return None
        
    except Exception as e:
        return None

def atualizar_noticias():
    print('🔄 Re-scrapando notícias...\n')
    
    noticias = Noticia.objects.all()
    atualizadas = 0
    falharam = 0
    
    for n in noticias:
        # Extrai a URL do rodapé
        url = extrair_url_do_rodape(n.conteudo)
        
        if not url:
            print(f'⚠️  ID {n.id}: Sem URL no rodapé')
            continue
        
        print(f'🔍 ID {n.id}: {n.titulo[:60]}...')
        
        # Tenta extrair conteúdo
        conteudo_novo = extrair_conteudo_completo(url)
        
        if conteudo_novo and len(conteudo_novo) > len(n.conteudo.split('---')[0]):
            # Preserva o rodapé original
            rodape_match = re.search(r'---\n.*', n.conteudo, re.DOTALL)
            rodape = rodape_match.group(0) if rodape_match else ''
            
            # Atualiza
            n.conteudo = conteudo_novo + '\n\n' + rodape
            n.save()
            
            print(f'   ✅ Atualizado: {len(n.conteudo.split("---")[0])} chars')
            atualizadas += 1
        else:
            print(f'   ❌ Falhou ou conteúdo menor')
            falharam += 1
    
    print(f'\n📊 Resumo:')
    print(f'   ✅ Atualizadas: {atualizadas}')
    print(f'   ❌ Falharam: {falharam}')
    print(f'   📝 Total: {noticias.count()}')

if __name__ == '__main__':
    atualizar_noticias()
