#!/usr/bin/env python
"""
Script para limpar notícias problemáticas:
- Sem imagem
- Com texto descontinuado (...)
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'claraboiacorp.settings')
django.setup()

from jcpemobile.models import Noticia

def limpar_noticias():
    print('🔍 Verificando notícias...\n')
    
    # Notícias sem imagem
    sem_imagem = []
    for n in Noticia.objects.all():
        if not n.imagem or not n.imagem.name:
            sem_imagem.append(n)
        else:
            # Verifica se o arquivo existe
            try:
                if not n.imagem.storage.exists(n.imagem.name):
                    sem_imagem.append(n)
            except:
                sem_imagem.append(n)
    
    print(f'❌ Notícias sem imagem ou com imagem quebrada: {len(sem_imagem)}')
    for n in sem_imagem:
        print(f'  ID {n.id}: {n.titulo[:70]}')
    
    # Notícias com texto descontinuado
    com_reticencias = []
    for n in Noticia.objects.all():
        # Procura por padrões de texto descontinuado
        if '...' in n.conteudo or '[...]' in n.conteudo:
            # Ignora se for no final (rodapé com autor/fonte)
            conteudo_limpo = n.conteudo.split('---')[0] if '---' in n.conteudo else n.conteudo
            if '...' in conteudo_limpo or '[...]' in conteudo_limpo:
                com_reticencias.append(n)
    
    print(f'\n❌ Notícias com texto descontinuado: {len(com_reticencias)}')
    for n in com_reticencias[:10]:
        print(f'  ID {n.id}: {n.titulo[:70]}')
    
    # Total para deletar
    para_deletar = list(set(sem_imagem + com_reticencias))
    print(f'\n🗑️  Total para deletar: {len(para_deletar)} notícias')
    
    if para_deletar:
        resposta = input('\n⚠️  Deseja deletar essas notícias? (s/N): ')
        if resposta.lower() == 's':
            ids = [n.id for n in para_deletar]
            Noticia.objects.filter(id__in=ids).delete()
            print(f'✅ {len(para_deletar)} notícias deletadas!')
            print(f'📊 Restam {Noticia.objects.count()} notícias no banco')
        else:
            print('❌ Operação cancelada')
    else:
        print('✅ Nenhuma notícia problemática encontrada!')

if __name__ == '__main__':
    limpar_noticias()
