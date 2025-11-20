"""
Script para adicionar todas as categorias no banco de dados
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'claraboiacorp.settings')
django.setup()

from jcpemobile.models import Categoria

# Lista de todas as categorias
categorias = [
    # Notícias Gerais
    "Notícias Gerais",
    "Brasil",
    "Política",
    "Economia",
    "Educação",
    "Saúde",
    "Ciência",
    "Internacional",
    "Mundo",
    "Cidades",
    "Segurança Pública",
    
    # Esportes
    "Esportes",
    "Futebol",
    "Brasileirão",
    "Copa do Brasil",
    "Libertadores",
    "Champions League",
    "UFC",
    "NBA",
    "Vôlei",
    "Fórmula 1",
    "Esportes Radicais",
    
    # Entretenimento
    "Entretenimento",
    "TV",
    "Famosos",
    "Cinema",
    "Música",
    "Reality Shows",
    "BBB",
    "A Fazenda",
    "Séries e Streaming",
    
    # Tecnologia
    "Tecnologia",
    "Inovação",
    "Inteligência Artificial",
    "Gadgets",
    "Segurança Digital",
    "Internet",
    "Games",
    
    # Economia / Mercado
    "Finanças Pessoais",
    "Investimentos",
    "Empreendedorismo",
    "Agronegócio",
    "Carreiras",
    "Concursos",
    
    # Automóveis
    "Automóveis",
    "Lançamentos",
    "Testes",
    "Dicas",
    "Mercado Automotivo",
    
    # Meio Ambiente
    "Meio Ambiente",
    "Clima",
    "Sustentabilidade",
    "Energia",
    
    # Categorias existentes (se não existirem ainda)
    "Culinária",
    "Global",
    "Nacional",
    
    # Temas Específicos
    "Violência",
    "Previsão do Tempo",
    "Desastres Naturais",
    "Eleições",
    "Fake News",
    "Cibersegurança",
    "Vacinação",
    "Inflação",
    "Impostos",
    "Redes Sociais",
    "Criptomoedas",
    "Metaverso",
    
    # Por Pessoas
    "Lula",
    "Bolsonaro",
    "Neymar",
    "Anitta",
    "Elon Musk",
    "Messi",
    "Celebridades",
    
    # Por Local
    "Recife",
    "São Paulo",
    "Rio de Janeiro",
    "Brasília",
    "Pernambuco",
    "Nordeste",
    "EUA",
    "Europa",
    
    # Por Organizações
    "STF",
    "Congresso",
    "MEC",
    "OMS",
    "Petrobras",
    "IBGE",
    "Apple",
    "Google",
    "Meta",
    "Microsoft",
]

def adicionar_categorias():
    """Adiciona todas as categorias no banco de dados"""
    categorias_adicionadas = 0
    categorias_existentes = 0
    
    print("Iniciando adição de categorias...")
    print("-" * 50)
    
    for nome_categoria in categorias:
        # Verificar se a categoria já existe
        categoria, criada = Categoria.objects.get_or_create(nome=nome_categoria)
        
        if criada:
            print(f"✓ Categoria criada: {nome_categoria}")
            categorias_adicionadas += 1
        else:
            print(f"- Categoria já existe: {nome_categoria}")
            categorias_existentes += 1
    
    print("-" * 50)
    print(f"\nResumo:")
    print(f"Categorias adicionadas: {categorias_adicionadas}")
    print(f"Categorias já existentes: {categorias_existentes}")
    print(f"Total de categorias: {Categoria.objects.count()}")
    print("\n✓ Processo concluído!")

if __name__ == "__main__":
    adicionar_categorias()
