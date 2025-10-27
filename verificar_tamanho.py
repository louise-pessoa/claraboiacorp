#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'claraboiacorp.settings')
django.setup()

from jcpemobile.models import Noticia

ultimas = Noticia.objects.order_by('-id')[:10]
print('📰 Últimas 10 notícias:\n')

for n in ultimas:
    tamanho = len(n.conteudo.split('---')[0])
    status = '✅' if tamanho > 1000 else '⚠️' if tamanho > 500 else '❌'
    print(f'{status} ID {n.id}: {tamanho:4d} chars - {n.titulo[:60]}...')

print(f'\n📊 Total de notícias: {Noticia.objects.count()}')
