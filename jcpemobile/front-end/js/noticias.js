/* ===================================================
   NOTICIAS.JS - JORNAL DO COMMERCIO
   Feed de Notícias e Interações
   =================================================== */

// ===================================================
// DADOS MOCKADOS
// ===================================================

const NOTICIAS_MOCK = [
    {
        id: 1,
        titulo: 'Governo de Pernambuco anuncia novo programa de educação digital',
        resumo: 'Iniciativa vai beneficiar mais de 500 mil estudantes da rede pública com tablets e acesso à internet.',
        categoria: 'educacao',
        imagem: 'https://picsum.photos/400/250?random=1',
        tempo: new Date(Date.now() - 2 * 3600000), // 2 horas atrás
        destaque: true
    },
    {
        id: 2,
        titulo: 'Sport vence clássico contra o Santa Cruz e assume liderança',
        resumo: 'Com gols de Jorginho e Gustavo Coutinho, Leão vence por 2 a 0 na Ilha do Retiro.',
        categoria: 'esportes',
        imagem: 'https://picsum.photos/400/250?random=2',
        tempo: new Date(Date.now() - 4 * 3600000), // 4 horas atrás
        destaque: false
    },
    {
        id: 3,
        titulo: 'Nova linha de metrô será inaugurada no próximo mês',
        resumo: 'Extensão vai conectar zona norte ao centro do Recife, beneficiando 200 mil passageiros por dia.',
        categoria: 'mobilidade',
        imagem: 'https://picsum.photos/400/250?random=3',
        tempo: new Date(Date.now() - 6 * 3600000), // 6 horas atrás
        destaque: false
    },
    {
        id: 4,
        titulo: 'Economia pernambucana cresce 4,5% no trimestre',
        resumo: 'Resultado supera média nacional e coloca o estado entre os que mais cresceram no período.',
        categoria: 'economia',
        imagem: 'https://picsum.photos/400/250?random=4',
        tempo: new Date(Date.now() - 8 * 3600000), // 8 horas atrás
        destaque: false
    },
    {
        id: 5,
        titulo: 'Festival de Inverno de Garanhuns divulga programação completa',
        resumo: 'Evento terá mais de 200 atrações culturais durante 10 dias de festa na Suíça Pernambucana.',
        categoria: 'cultura',
        imagem: 'https://picsum.photos/400/250?random=5',
        tempo: new Date(Date.now() - 24 * 3600000), // 1 dia atrás
        destaque: false
    }
];

// Mais notícias para simular paginação
const MAIS_NOTICIAS = [
    {
        id: 6,
        titulo: 'Prefeitura do Recife anuncia concurso com 500 vagas',
        resumo: 'Oportunidades para níveis médio e superior em diversas áreas.',
        categoria: 'pernambuco',
        imagem: 'https://picsum.photos/400/250?random=6',
        tempo: new Date(Date.now() - 26 * 3600000)
    },
    {
        id: 7,
        titulo: 'Pesquisa mostra intenção de votos para eleições municipais',
        resumo: 'Levantamento aponta cenários para disputa pela prefeitura da capital.',
        categoria: 'politica',
        imagem: 'https://picsum.photos/400/250?random=7',
        tempo: new Date(Date.now() - 28 * 3600000)
    },
    {
        id: 8,
        titulo: 'Chuvas devem voltar ao estado na próxima semana',
        resumo: 'Meteorologia prevê precipitações em todas as regiões de Pernambuco.',
        categoria: 'pernambuco',
        imagem: 'https://picsum.photos/400/250?random=8',
        tempo: new Date(Date.now() - 30 * 3600000)
    }
];

// ===================================================
// INICIALIZAÇÃO
// ===================================================

document.addEventListener('DOMContentLoaded', () => {
    inicializarNoticias();
});

function inicializarNoticias() {
    // Carregar notícias iniciais
    carregarNoticiasIniciais();

    // Configurar botão carregar mais
    configurarCarregarMais();

    // Configurar interações dos cards
    configurarInteracoesCards();

    // Configurar auto-refresh
    configurarAutoRefresh();
}

// ===================================================
// CARREGAR NOTÍCIAS
// ===================================================

function carregarNoticiasIniciais() {
    const feedNoticias = document.getElementById('feedNoticias');

    if (!feedNoticias) return;

    // Limpar placeholder
    feedNoticias.innerHTML = '';

    // Renderizar notícias
    NOTICIAS_MOCK.forEach((noticia, index) => {
        const card = criarCardNoticia(noticia, index === 0);
        feedNoticias.appendChild(card);
    });

    // Animar entrada
    animarEntradaCards();
}

function criarCardNoticia(noticia, isDestaque = false) {
    const article = document.createElement('article');
    article.className = `cartao-noticia ${isDestaque ? 'cartao-noticia--destaque' : ''}`;
    article.dataset.id = noticia.id;

    article.innerHTML = `
        <div class="cartao-imagem">
            <img src="${noticia.imagem}"
                 alt="${noticia.titulo}"
                 loading="lazy">
            <span class="badge-categoria badge-${noticia.categoria}">
                ${obterNomeCategoria(noticia.categoria)}
            </span>
        </div>
        <div class="cartao-conteudo">
            <h2 class="cartao-titulo">${noticia.titulo}</h2>
            <p class="cartao-resumo">${noticia.resumo}</p>
            <div class="cartao-rodape">
                <time class="cartao-tempo" datetime="${noticia.tempo.toISOString()}">
                    ${window.JC.utils.formatarData(noticia.tempo)}
                </time>
                <div class="cartao-acoes">
                    <button class="botao-salvar" aria-label="Salvar notícia">
                        <i class="far fa-bookmark"></i>
                    </button>
                    <button class="botao-compartilhar" aria-label="Compartilhar">
                        <i class="fas fa-share-alt"></i>
                    </button>
                </div>
            </div>
        </div>
    `;

    return article;
}

function obterNomeCategoria(categoria) {
    const categorias = {
        pernambuco: 'Pernambuco',
        politica: 'Política',
        economia: 'Economia',
        esportes: 'Esportes',
        cultura: 'Cultura',
        educacao: 'Educação',
        mobilidade: 'Mobilidade',
        mundo: 'Mundo'
    };

    return categorias[categoria] || categoria;
}

// ===================================================
// CARREGAR MAIS
// ===================================================

function configurarCarregarMais() {
    const botaoCarregarMais = document.getElementById('botaoCarregarMais');

    if (!botaoCarregarMais) return;

    botaoCarregarMais.addEventListener('click', carregarMaisNoticias);
}

function carregarMaisNoticias() {
    const botao = document.getElementById('botaoCarregarMais');
    const feedNoticias = document.getElementById('feedNoticias');

    // Mostrar loading
    botao.classList.add('carregando');
    botao.innerHTML = `
        <span>Carregando...</span>
        <div class="spinner-pequeno"></div>
    `;

    // Simular carregamento
    setTimeout(() => {
        // Adicionar mais notícias
        MAIS_NOTICIAS.forEach(noticia => {
            const card = criarCardNoticia(noticia);
            feedNoticias.appendChild(card);
        });

        // Restaurar botão
        botao.classList.remove('carregando');
        botao.innerHTML = `
            <span>Carregar mais notícias</span>
            <i class="fas fa-arrow-down"></i>
        `;

        // Animar entrada dos novos cards
        animarEntradaCards(true);

        // Incrementar página
        window.JC.state.paginaAtual++;

        // Se não houver mais, esconder botão
        if (window.JC.state.paginaAtual >= 3) {
            botao.style.display = 'none';
            mostrarFimDoFeed();
        }
    }, 1000);
}

function mostrarFimDoFeed() {
    const container = document.querySelector('.carregar-mais-container');
    container.innerHTML = `
        <div class="fim-do-feed">
            <i class="fas fa-check-circle"></i>
            <p>Você está em dia com as notícias!</p>
        </div>
    `;
}

// ===================================================
// INTERAÇÕES DOS CARDS
// ===================================================

function configurarInteracoesCards() {
    // Delegar eventos para o feed
    const feedNoticias = document.getElementById('feedNoticias');

    if (!feedNoticias) return;

    // Click no card
    feedNoticias.addEventListener('click', (e) => {
        const card = e.target.closest('.cartao-noticia');
        const botaoSalvar = e.target.closest('.botao-salvar');
        const botaoCompartilhar = e.target.closest('.botao-compartilhar');

        if (botaoSalvar) {
            e.stopPropagation();
            toggleSalvarNoticia(card);
        } else if (botaoCompartilhar) {
            e.stopPropagation();
            compartilharNoticia(card);
        } else if (card) {
            abrirNoticia(card);
        }
    });

    // Hover effects para desktop
    feedNoticias.addEventListener('mouseenter', (e) => {
        if (e.target.classList.contains('cartao-noticia')) {
            e.target.classList.add('hover');
        }
    }, true);

    feedNoticias.addEventListener('mouseleave', (e) => {
        if (e.target.classList.contains('cartao-noticia')) {
            e.target.classList.remove('hover');
        }
    }, true);
}

// ===================================================
// SALVAR NOTÍCIAS
// ===================================================

function toggleSalvarNoticia(card) {
    const botaoSalvar = card.querySelector('.botao-salvar');
    const icone = botaoSalvar.querySelector('i');
    const noticiaId = card.dataset.id;

    // Toggle estado
    const isSalvo = icone.classList.contains('fas');

    if (isSalvo) {
        // Remover dos salvos
        icone.classList.remove('fas');
        icone.classList.add('far');
        removerNoticiaSalva(noticiaId);
        mostrarToast('Notícia removida dos salvos', 'info');
    } else {
        // Adicionar aos salvos
        icone.classList.add('fas');
        icone.classList.remove('far');
        salvarNoticia(noticiaId);
        mostrarToast('Notícia salva com sucesso!', 'sucesso');

        // Animação
        animarSalvar(botaoSalvar);
    }
}

function salvarNoticia(noticiaId) {
    let salvos = window.JC.state.noticiasSalvas;
    if (!salvos.includes(noticiaId)) {
        salvos.push(noticiaId);
        window.JC.utils.salvarDadosLocais('noticiasSalvas', salvos);
    }
}

function removerNoticiaSalva(noticiaId) {
    let salvos = window.JC.state.noticiasSalvas;
    salvos = salvos.filter(id => id !== noticiaId);
    window.JC.state.noticiasSalvas = salvos;
    window.JC.utils.salvarDadosLocais('noticiasSalvas', salvos);
}

function animarSalvar(botao) {
    botao.classList.add('animacao-salvar');
    setTimeout(() => {
        botao.classList.remove('animacao-salvar');
    }, 600);
}

// ===================================================
// COMPARTILHAR
// ===================================================

function compartilharNoticia(card) {
    const titulo = card.querySelector('.cartao-titulo').textContent;
    const url = window.location.href + '#noticia-' + card.dataset.id;

    if (navigator.share) {
        // API nativa de compartilhamento
        navigator.share({
            title: titulo,
            text: 'Veja esta notícia do Jornal do Commercio',
            url: url
        }).catch(err => console.log('Compartilhamento cancelado'));
    } else {
        // Fallback - mostrar opções
        mostrarOpcoesCompartilhamento(titulo, url);
    }
}

function mostrarOpcoesCompartilhamento(titulo, url) {
    const modal = document.createElement('div');
    modal.className = 'modal-compartilhar';
    modal.innerHTML = `
        <div class="modal-conteudo">
            <h3>Compartilhar notícia</h3>
            <div class="opcoes-compartilhar">
                <button data-rede="whatsapp">
                    <i class="fab fa-whatsapp"></i>
                    WhatsApp
                </button>
                <button data-rede="facebook">
                    <i class="fab fa-facebook"></i>
                    Facebook
                </button>
                <button data-rede="twitter">
                    <i class="fab fa-twitter"></i>
                    Twitter
                </button>
                <button data-rede="copiar">
                    <i class="fas fa-link"></i>
                    Copiar link
                </button>
            </div>
            <button class="modal-fechar">Fechar</button>
        </div>
    `;

    document.body.appendChild(modal);

    // Eventos
    modal.querySelectorAll('[data-rede]').forEach(btn => {
        btn.addEventListener('click', () => {
            compartilharEm(btn.dataset.rede, titulo, url);
            modal.remove();
        });
    });

    modal.querySelector('.modal-fechar').addEventListener('click', () => {
        modal.remove();
    });

    // Animar entrada
    requestAnimationFrame(() => {
        modal.classList.add('ativo');
    });
}

function compartilharEm(rede, titulo, url) {
    const urls = {
        whatsapp: `https://wa.me/?text=${encodeURIComponent(titulo + ' ' + url)}`,
        facebook: `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(url)}`,
        twitter: `https://twitter.com/intent/tweet?text=${encodeURIComponent(titulo)}&url=${encodeURIComponent(url)}`,
        copiar: url
    };

    if (rede === 'copiar') {
        navigator.clipboard.writeText(url);
        mostrarToast('Link copiado!', 'sucesso');
    } else {
        window.open(urls[rede], '_blank');
    }
}

// ===================================================
// ABRIR NOTÍCIA
// ===================================================

function abrirNoticia(card) {
    const noticiaId = card.dataset.id;
    console.log('Abrindo notícia:', noticiaId);

    // Animação de click
    card.classList.add('clicado');
    setTimeout(() => {
        card.classList.remove('clicado');
    }, 300);

    // Em produção, navegaria para a página da notícia
    // Por enquanto, mostrar preview
    mostrarPreviewNoticia(noticiaId);
}

function mostrarPreviewNoticia(noticiaId) {
    // Simular carregamento da notícia completa
    mostrarToast('Carregando notícia completa...', 'info');
}

// ===================================================
// AUTO-REFRESH
// ===================================================

function configurarAutoRefresh() {
    // Verificar novas notícias a cada 5 minutos
    setInterval(() => {
        verificarNovasNoticias();
    }, 5 * 60 * 1000);
}

function verificarNovasNoticias() {
    console.log('Verificando novas notícias...');

    // Em produção, faria uma chamada API
    // Por enquanto, apenas simular
    const temNovasNoticias = Math.random() > 0.7;

    if (temNovasNoticias) {
        mostrarBotaoNovasNoticias();
    }
}

function mostrarBotaoNovasNoticias() {
    const header = document.getElementById('cabecalho');

    if (document.getElementById('botaoNovasNoticias')) return;

    const botao = document.createElement('button');
    botao.id = 'botaoNovasNoticias';
    botao.className = 'botao-novas-noticias';
    botao.innerHTML = `
        <i class="fas fa-arrow-up"></i>
        <span>Novas notícias disponíveis</span>
    `;

    header.appendChild(botao);

    botao.addEventListener('click', () => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
        location.reload();
    });
}

// ===================================================
// ANIMAÇÕES
// ===================================================

function animarEntradaCards(apenasNovos = false) {
    const cards = apenasNovos
        ? document.querySelectorAll('.cartao-noticia:not(.animado)')
        : document.querySelectorAll('.cartao-noticia');

    cards.forEach((card, index) => {
        setTimeout(() => {
            card.classList.add('animado');
        }, index * 100);
    });
}

// ===================================================
// TOAST NOTIFICATIONS
// ===================================================

function mostrarToast(mensagem, tipo = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast toast-${tipo}`;
    toast.textContent = mensagem;

    document.body.appendChild(toast);

    requestAnimationFrame(() => {
        toast.classList.add('visivel');
    });

    setTimeout(() => {
        toast.classList.remove('visivel');
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// ===================================================
// ESTILOS ADICIONAIS
// ===================================================

const styleNoticias = document.createElement('style');
styleNoticias.textContent = `
    .cartao-noticia {
        opacity: 0;
        transform: translateY(20px);
        transition: all 0.4s ease;
    }

    .cartao-noticia.animado {
        opacity: 1;
        transform: translateY(0);
    }

    .cartao-noticia.clicado {
        transform: scale(0.98);
    }

    .cartao-noticia.hover .cartao-imagem img {
        transform: scale(1.05);
    }

    .cartao-acoes {
        display: flex;
        gap: 8px;
    }

    .botao-salvar, .botao-compartilhar {
        width: 32px;
        height: 32px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: #F3F4F6;
        border-radius: 50%;
        color: #6B7280;
        transition: all 0.2s;
    }

    .botao-salvar:hover, .botao-compartilhar:hover {
        background: #DC2626;
        color: white;
    }

    .botao-salvar.animacao-salvar {
        animation: salvar 0.6s ease;
    }

    @keyframes salvar {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.2); }
    }

    .spinner-pequeno {
        width: 16px;
        height: 16px;
        border: 2px solid white;
        border-top-color: transparent;
        border-radius: 50%;
        animation: spin 0.8s linear infinite;
    }

    .fim-do-feed {
        text-align: center;
        padding: 32px;
        color: #10B981;
    }

    .fim-do-feed i {
        font-size: 48px;
        margin-bottom: 16px;
    }

    .modal-compartilhar {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0,0,0,0.5);
        display: flex;
        align-items: flex-end;
        justify-content: center;
        opacity: 0;
        transition: opacity 0.3s;
        z-index: 1000;
    }

    .modal-compartilhar.ativo {
        opacity: 1;
    }

    .modal-compartilhar .modal-conteudo {
        background: white;
        border-radius: 16px 16px 0 0;
        padding: 24px;
        width: 100%;
        max-width: 500px;
        transform: translateY(100%);
        transition: transform 0.3s;
    }

    .modal-compartilhar.ativo .modal-conteudo {
        transform: translateY(0);
    }

    .opcoes-compartilhar {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 12px;
        margin: 24px 0;
    }

    .opcoes-compartilhar button {
        padding: 12px;
        background: #F3F4F6;
        border-radius: 8px;
        display: flex;
        align-items: center;
        gap: 8px;
        justify-content: center;
        font-size: 14px;
    }

    .botao-novas-noticias {
        position: fixed;
        top: 70px;
        left: 50%;
        transform: translateX(-50%);
        background: #DC2626;
        color: white;
        padding: 8px 16px;
        border-radius: 20px;
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 14px;
        z-index: 1000;
        animation: slideDown 0.3s ease;
    }

    @keyframes slideDown {
        from { transform: translate(-50%, -100%); }
        to { transform: translate(-50%, 0); }
    }

    .toast {
        position: fixed;
        bottom: 80px;
        left: 50%;
        transform: translateX(-50%) translateY(100px);
        padding: 12px 24px;
        border-radius: 8px;
        color: white;
        font-weight: 500;
        transition: transform 0.3s;
        z-index: 1000;
    }

    .toast.visivel {
        transform: translateX(-50%) translateY(0);
    }

    .toast-info { background: #3B82F6; }
    .toast-sucesso { background: #10B981; }
    .toast-erro { background: #EF4444; }
`;
document.head.appendChild(styleNoticias);