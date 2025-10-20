import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'claraboiacorp.settings')
django.setup()

from jcpemobile.models import Categoria, Autor, Noticia

# Criar categorias
categorias_data = [
    'Pernambuco', 'Política', 'Economia', 'Esportes',
    'Cultura', 'Mundo', 'Educação', 'Mobilidade'
]

categorias = {}
for nome in categorias_data:
    cat, created = Categoria.objects.get_or_create(nome=nome)
    categorias[nome] = cat
    print(f"Categoria '{nome}' {'criada' if created else 'já existe'}")

# Criar autor
autor, created = Autor.objects.get_or_create(
    nome='Redação JC',
    defaults={'bio': 'Equipe de jornalismo do Jornal do Commercio'}
)
print(f"\nAutor '{autor.nome}' {'criado' if created else 'já existe'}")

# Criar notícias de exemplo
noticias_data = [
    {
        'titulo': 'Recife anuncia novo plano de mobilidade urbana para 2025',
        'resumo': 'Prefeitura apresenta projeto que inclui novas ciclovias e corredores exclusivos para ônibus',
        'conteudo': 'A Prefeitura do Recife anunciou hoje um ambicioso plano de mobilidade urbana para 2025. O projeto inclui a construção de 50km de novas ciclovias, além da criação de corredores exclusivos para ônibus nas principais avenidas da cidade. Segundo o prefeito, o objetivo é reduzir o tempo de deslocamento e incentivar o uso de transporte público e meios alternativos.',
        'categoria': categorias['Mobilidade']
    },
    {
        'titulo': 'Governador anuncia pacote de investimentos em infraestrutura',
        'resumo': 'Estado vai investir R$ 500 milhões em obras de infraestrutura em todo Pernambuco',
        'conteudo': 'O governador de Pernambuco anunciou um pacote de investimentos de R$ 500 milhões voltado para obras de infraestrutura em todo o estado. Os recursos serão destinados à recuperação de estradas, construção de pontes e modernização de equipamentos públicos.',
        'categoria': categorias['Política']
    },
    {
        'titulo': 'Porto Digital abre 500 novas vagas em tecnologia',
        'resumo': 'Empresas do Porto Digital estão contratando profissionais para diversas áreas da tecnologia',
        'conteudo': 'O Porto Digital do Recife anunciou a abertura de 500 novas vagas para profissionais de tecnologia. As oportunidades são para desenvolvedores, designers, analistas de dados e gerentes de projeto. As empresas oferecem salários competitivos e benefícios atrativos.',
        'categoria': categorias['Economia']
    },
    {
        'titulo': 'Sport vence clássico e se aproxima do G4 do campeonato',
        'resumo': 'Time rubro-negro venceu o clássico estadual por 2 a 1 na Ilha do Retiro',
        'conteudo': 'O Sport Club do Recife venceu o clássico estadual por 2 a 1 jogando na Ilha do Retiro. Com o resultado, o time rubro-negro se aproxima do G4 do campeonato brasileiro e ganha moral para os próximos jogos da temporada.',
        'categoria': categorias['Esportes']
    },
    {
        'titulo': 'Carnaval 2025: Recife divulga programação oficial',
        'resumo': 'Programação conta com mais de 200 apresentações espalhadas pela cidade',
        'conteudo': 'A Prefeitura do Recife divulgou a programação oficial do Carnaval 2025. Serão mais de 200 apresentações espalhadas por diversos pontos da cidade, com destaque para os polos do Recife Antigo, Boa Vista e Imbiribeira. A folia começa no dia 1º de março.',
        'categoria': categorias['Cultura']
    },
    {
        'titulo': 'UFPE divulga lista de aprovados no vestibular 2025',
        'resumo': 'Mais de 6 mil estudantes foram aprovados nos cursos de graduação',
        'conteudo': 'A Universidade Federal de Pernambuco (UFPE) divulgou a lista de aprovados no vestibular 2025. Ao todo, mais de 6 mil estudantes conquistaram uma vaga nos diversos cursos de graduação oferecidos pela instituição. As matrículas começam na próxima semana.',
        'categoria': categorias['Educação']
    },
    {
        'titulo': 'Cúpula do clima define novas metas para 2030',
        'resumo': 'Países se comprometem a reduzir emissões de carbono em 50% até o final da década',
        'conteudo': 'A Cúpula do Clima realizada em Dubai definiu novas metas ambiciosas para 2030. Os países participantes se comprometeram a reduzir as emissões de carbono em pelo menos 50% até o final da década, além de aumentar investimentos em energias renováveis.',
        'categoria': categorias['Mundo']
    },
    {
        'titulo': 'Nova linha de metrô chega ao bairro de Boa Viagem',
        'resumo': 'Obras da nova linha Sul do metrô estão 80% concluídas',
        'conteudo': 'As obras da nova linha Sul do metrô do Recife, que vai atender o bairro de Boa Viagem, estão 80% concluídas. A previsão é que a linha entre em operação no segundo semestre de 2025, beneficiando milhares de moradores da zona sul da cidade.',
        'categoria': categorias['Mobilidade']
    },
    {
        'titulo': 'Projeto de revitalização do Cais José Estelita avança',
        'resumo': 'Novo projeto prevê área de lazer e preservação ambiental',
        'conteudo': 'O projeto de revitalização do Cais José Estelita ganhou novo impulso. A nova proposta, elaborada em conjunto com a sociedade civil, prevê a criação de uma grande área de lazer com preservação ambiental, além de espaços culturais e ciclovias.',
        'categoria': categorias['Pernambuco']
    },
    {
        'titulo': 'Festival de cinema internacional começa em Olinda',
        'resumo': 'Evento reúne produções de mais de 30 países',
        'conteudo': 'Começa hoje em Olinda o Festival Internacional de Cinema. O evento, que vai até o dia 25, reúne produções de mais de 30 países e oferece sessões gratuitas em diversos pontos da cidade histórica. A programação completa está disponível no site oficial.',
        'categoria': categorias['Cultura']
    }
]

print("\nCriando notícias...\n")
for noticia_data in noticias_data:
    noticia, created = Noticia.objects.get_or_create(
        titulo=noticia_data['titulo'],
        defaults={
            'resumo': noticia_data['resumo'],
            'conteudo': noticia_data['conteudo'],
            'categoria': noticia_data['categoria'],
            'autor': autor
        }
    )
    if created:
        print(f"[OK] Criada: {noticia.titulo}")
        print(f"  Slug: {noticia.slug}")
    else:
        print(f"[--] Ja existe: {noticia.titulo}")

print(f"\n[OK] Total de noticias no banco: {Noticia.objects.count()}")
