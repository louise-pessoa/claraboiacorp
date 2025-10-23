/* ===================================================
   NAVEGACAO.JS - JORNAL DO COMMERCIO
   Menu Lateral, Navegação e Interações
   =================================================== */

// ===================================================
// INICIALIZAÇÃO
// ===================================================

document.addEventListener('DOMContentLoaded', () => {
    inicializarNavegacao();
});

function inicializarNavegacao() {
    // Verificar se o objeto JC existe, senão criar
    if (!window.JC) {
        window.JC = {
            state: {
                menuAberto: false,
                noticiasSalvas: []
            }
        };
    }

    // Menu hamburguer
    configurarMenuHamburguer();

    // Menu lateral
    configurarMenuLateral();

    // Navegação inferior
    configurarNavegacaoInferior();

    // Submenus - IMPORTANTE: deve ser configurado após o menu lateral
    configurarSubmenus();

    // Scroll suave
    configurarScrollSuave();

    // Log para debug
    console.log('Navegação inicializada com sucesso');
}

// ===================================================
// MENU HAMBURGUER
// ===================================================

function configurarMenuHamburguer() {
    const menuHamburguer = document.getElementById('menuHamburguer');
    const menuLateral = document.getElementById('menuLateral');
    const menuOverlay = document.getElementById('menuOverlay');

    console.log('Configurando menu hamburguer...');
    console.log('menuHamburguer:', menuHamburguer);
    console.log('menuLateral:', menuLateral);
    console.log('menuOverlay:', menuOverlay);

    if (!menuHamburguer || !menuLateral) {
        console.error('Elementos do menu não encontrados!');
        return;
    }

    menuHamburguer.addEventListener('click', (e) => {
        console.log('Menu hamburguer clicado!');
        e.stopPropagation();
        toggleMenu();
    });

    // Fechar menu
    const menuFechar = document.getElementById('menuLateralFechar');
    if (menuFechar) {
        menuFechar.addEventListener('click', (e) => {
            e.stopPropagation();
            fecharMenu();
        });
    }

    // Overlay - fechar ao clicar no overlay (fundo escuro)
    if (menuOverlay) {
        menuOverlay.addEventListener('click', fecharMenu);
    }

    // Adicionar evento global para fechar menu ao clicar fora
    document.addEventListener('click', (e) => {
        const menuAberto = menuLateral.classList.contains('ativo');

        // Se o menu está aberto e o clique foi fora do menu e do botão hamburguer
        if (menuAberto &&
            !menuLateral.contains(e.target) &&
            !menuHamburguer.contains(e.target)) {
            fecharMenu();
        }
    });
}

function toggleMenu() {
    const menuLateral = document.getElementById('menuLateral');
    const menuOverlay = document.getElementById('menuOverlay');
    const menuHamburguer = document.getElementById('menuHamburguer');
    const isAberto = menuLateral.classList.contains('ativo');

    console.log('toggleMenu chamado. Menu está aberto?', isAberto);

    if (isAberto) {
        fecharMenu();
    } else {
        abrirMenu();
    }
}

function abrirMenu() {
    const menuLateral = document.getElementById('menuLateral');
    const menuOverlay = document.getElementById('menuOverlay');
    const menuHamburguer = document.getElementById('menuHamburguer');

    menuLateral.classList.add('ativo');
    menuOverlay.classList.add('ativo');
    menuHamburguer.classList.add('ativo');
    document.body.style.overflow = 'hidden';

    window.JC.state.menuAberto = true;

    // Animação de entrada dos itens do menu
    animarItensMenu();

    // Adicionar proteção extra contra fechamento acidental
    // Aguardar um pequeno delay antes de permitir fechamento
    menuLateral.dataset.podeFechar = 'false';
    setTimeout(() => {
        menuLateral.dataset.podeFechar = 'true';
    }, 300);
}

function fecharMenu() {
    const menuLateral = document.getElementById('menuLateral');
    const menuOverlay = document.getElementById('menuOverlay');
    const menuHamburguer = document.getElementById('menuHamburguer');

    // Verificar se pode fechar (evita fechamento muito rápido)
    if (menuLateral && menuLateral.dataset.podeFechar === 'false') {
        return;
    }

    menuLateral.classList.remove('ativo');
    menuOverlay.classList.remove('ativo');
    menuHamburguer.classList.remove('ativo');
    document.body.style.overflow = '';

    window.JC.state.menuAberto = false;

    // Fechar todos os submenus
    fecharTodosSubmenus();

    // Resetar o flag de pode fechar
    if (menuLateral) {
        menuLateral.dataset.podeFechar = 'true';
    }
}

function animarItensMenu() {
    const itens = document.querySelectorAll('.menu-item');
    itens.forEach((item, index) => {
        item.style.animation = `slideInLeft 0.3s ${index * 0.05}s ease-out forwards`;
    });
}

// ===================================================
// MENU LATERAL
// ===================================================

function configurarMenuLateral() {
    // IMPORTANTE: Prevenir que cliques dentro do menu fechem ele
    const menuLateral = document.getElementById('menuLateral');

    if (!menuLateral) return;

    // Prevenir propagação apenas para fechar o menu, mas não bloquear eventos internos
    menuLateral.addEventListener('click', (e) => {
        e.stopPropagation();
    }, false);

    // Links do menu principal (que NÃO são botões de submenu)
    const menuLinks = document.querySelectorAll('.menu-lateral .menu-link');

    menuLinks.forEach(link => {
        // Se não for expansível (não tem submenu) - estes são links normais
        if (!link.closest('.menu-item-expansivel')) {
            link.addEventListener('click', (e) => {
                const linkHref = link.getAttribute('href');
                
                // Se o link tem uma URL real (não é âncora #), permitir navegação
                if (linkHref && !linkHref.startsWith('#')) {
                    // Permitir que o navegador siga o link normalmente
                    return;
                }
                
                // Para âncoras (#), prevenir comportamento padrão
                e.preventDefault();
                e.stopPropagation();

                // Marcar como ativo
                marcarMenuAtivo(link);

                // Adicionar feedback visual
                link.style.transform = 'scale(0.98)';
                setTimeout(() => {
                    link.style.transform = '';
                }, 200);

                // Aqui você pode adicionar navegação futura
                const href = link.getAttribute('href');
                console.log('Navegando para:', href);

                // NÃO fechar o menu - só fecha com X ou clicando fora
            });
        }
        // Se for expansível, será tratado pela função configurarSubmenus()
    });

    // Configurar links dentro dos submenus
    const submenuLinks = document.querySelectorAll('.submenu a');
    submenuLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            const linkHref = link.getAttribute('href');
            
            // Se o link tem uma URL real (não é âncora #), permitir navegação
            if (linkHref && !linkHref.startsWith('#')) {
                // Permitir que o navegador siga o link normalmente
                return;
            }
            
            // Para âncoras (#), prevenir comportamento padrão
            e.preventDefault();
            e.stopPropagation();

            // Marcar submenu item como selecionado
            document.querySelectorAll('.submenu a').forEach(a => a.classList.remove('ativo'));
            link.classList.add('ativo');

            // Feedback visual
            link.style.transform = 'scale(0.98)';
            setTimeout(() => {
                link.style.transform = '';
            }, 200);

            // Aqui você pode adicionar navegação futura
            console.log('Navegando para submenu:', linkHref);

            // NÃO fechar o menu automaticamente
        });
    });

    // Swipe para fechar (mobile)
    configurarSwipeMenu();
}

function marcarMenuAtivo(linkAtivo) {
    // Remover ativo de todos
    document.querySelectorAll('.menu-lateral .menu-link').forEach(link => {
        link.classList.remove('ativo');
    });

    // Adicionar ativo ao clicado
    linkAtivo.classList.add('ativo');
}

// ===================================================
// SUBMENUS
// ===================================================

function configurarSubmenus() {
    console.log('Configurando submenus...');

    const menuItensExpansiveis = document.querySelectorAll('.menu-item-expansivel');
    console.log('Itens expansíveis encontrados:', menuItensExpansiveis.length);

    menuItensExpansiveis.forEach((item, index) => {
        const botao = item.querySelector('.menu-link');
        const submenu = item.querySelector('.submenu');

        if (!botao || !submenu) {
            console.error(`Problema no item ${index}: botão ou submenu não encontrado`);
            return;
        }

        console.log(`Configurando submenu ${index}:`, {
            texto: botao.querySelector('span')?.textContent,
            temSubmenu: !!submenu
        });

        // Configurar como botão
        if (botao.tagName === 'BUTTON') {
            botao.type = 'button';
        }
        botao.style.cursor = 'pointer';

        // Estado inicial
        botao.setAttribute('aria-expanded', 'false');
        submenu.classList.remove('ativo');
        submenu.style.display = 'none';

        // Evento de clique único e simples
        botao.addEventListener('click', function(e) {
            // Não usar preventDefault para não bloquear o evento
            e.stopPropagation();

            console.log('Clique no submenu:', botao.querySelector('span')?.textContent);

            const isAberto = botao.getAttribute('aria-expanded') === 'true';

            if (isAberto) {
                // Fechar
                botao.setAttribute('aria-expanded', 'false');
                submenu.style.display = 'none';
                submenu.classList.remove('ativo');

                // Rotacionar seta
                const seta = botao.querySelector('.menu-seta');
                if (seta) {
                    seta.style.transform = '';
                }

                console.log('Submenu fechado');
            } else {
                // Fechar outros submenus
                document.querySelectorAll('.menu-item-expansivel').forEach(outroItem => {
                    const outroBotao = outroItem.querySelector('.menu-link');
                    const outroSubmenu = outroItem.querySelector('.submenu');
                    if (outroBotao && outroSubmenu && outroBotao !== botao) {
                        outroBotao.setAttribute('aria-expanded', 'false');
                        outroSubmenu.style.display = 'none';
                        outroSubmenu.classList.remove('ativo');

                        const outraSeta = outroBotao.querySelector('.menu-seta');
                        if (outraSeta) {
                            outraSeta.style.transform = '';
                        }
                    }
                });

                // Abrir este submenu
                botao.setAttribute('aria-expanded', 'true');
                submenu.style.display = 'block';

                // Pequeno delay para animação funcionar
                setTimeout(() => {
                    submenu.classList.add('ativo');
                }, 10);

                // Rotacionar seta
                const seta = botao.querySelector('.menu-seta');
                if (seta) {
                    seta.style.transform = 'rotate(180deg)';
                }

                console.log('Submenu aberto');
            }
        });

        // Suporte ao teclado
        botao.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                botao.click();
            }
        });
    });

    console.log('Configuração de submenus concluída');
}

// Função auxiliar para fechar todos os submenus
// (mantida pois é usada em outros lugares)

function fecharTodosSubmenus() {
    document.querySelectorAll('.menu-item-expansivel').forEach(item => {
        const botao = item.querySelector('.menu-link');
        const submenu = item.querySelector('.submenu');

        if (botao && submenu) {
            botao.setAttribute('aria-expanded', 'false');
            submenu.style.display = 'none';
            submenu.classList.remove('ativo');

            const seta = botao.querySelector('.menu-seta');
            if (seta) {
                seta.style.transform = '';
            }
        }
    });
}

// ===================================================
// NAVEGAÇÃO INFERIOR
// ===================================================

function configurarNavegacaoInferior() {
    const navItens = document.querySelectorAll('.navegacao-inferior .nav-item');

    navItens.forEach(item => {
        item.addEventListener('click', (e) => {
            const itemHref = item.getAttribute('href');
            
            // Se o link tem uma URL real (não é âncora #), permitir navegação
            if (itemHref && !itemHref.startsWith('#')) {
                // Permitir que o navegador siga o link normalmente
                return;
            }
            
            // Para âncoras (#), prevenir comportamento padrão
            e.preventDefault();

            // Remover ativo de todos
            navItens.forEach(i => i.classList.remove('nav-item-ativo'));

            // Adicionar ativo ao clicado
            item.classList.add('nav-item-ativo');

            // Ação baseada no item
            executarAcaoNavegacao(itemHref);

            // Feedback tátil
            if (navigator.vibrate) {
                navigator.vibrate(10);
            }
        });
    });
}

function executarAcaoNavegacao(href) {
    switch(href) {
        case '#home':
            window.scrollTo({ top: 0, behavior: 'smooth' });
            break;
        case '#categorias':
            abrirMenu();
            break;
        case '#salvos':
            mostrarNoticiasSalvas();
            break;
        case '#perfil':
            mostrarPerfil();
            break;
    }
}

// ===================================================
// SWIPE GESTURES
// ===================================================

function configurarSwipeMenu() {
    const menuLateral = document.getElementById('menuLateral');

    if (!menuLateral) return;

    let startX = 0;
    let currentX = 0;
    let isDragging = false;
    let startTime = 0;

    menuLateral.addEventListener('touchstart', (e) => {
        startX = e.touches[0].clientX;
        currentX = startX;
        isDragging = true;
        startTime = Date.now();

        // Prevenir que o toque inicial feche o menu
        e.stopPropagation();
    }, { passive: true });

    menuLateral.addEventListener('touchmove', (e) => {
        if (!isDragging) return;

        currentX = e.touches[0].clientX;
        const deltaX = startX - currentX;

        // Se swipe para esquerda e maior que 20px
        if (deltaX > 20) {
            // Aplicar transformação suave
            const translateX = Math.min(deltaX * 0.8, 200);
            menuLateral.style.transform = `translateX(-${translateX}px)`;
            menuLateral.style.transition = 'none';
        }
    }, { passive: true });

    menuLateral.addEventListener('touchend', (e) => {
        if (!isDragging) return;

        const deltaX = startX - currentX;
        const deltaTime = Date.now() - startTime;
        const velocity = Math.abs(deltaX) / deltaTime;

        // Restaurar transição
        menuLateral.style.transition = '';

        // Fechar se:
        // 1. Swipe rápido (velocidade > 0.5 px/ms) com pelo menos 50px de distância
        // 2. Ou swipe longo (> 100px)
        if ((velocity > 0.5 && deltaX > 50) || deltaX > 100) {
            fecharMenu();
        } else {
            // Voltar à posição original
            menuLateral.style.transform = '';
        }

        isDragging = false;
    }, { passive: true });

    // Cancelar swipe se o toque sair da área
    menuLateral.addEventListener('touchcancel', (e) => {
        if (isDragging) {
            menuLateral.style.transform = '';
            menuLateral.style.transition = '';
            isDragging = false;
        }
    }, { passive: true });
}

// ===================================================
// SCROLL SUAVE
// ===================================================

function configurarScrollSuave() {
    // Links com hash - apenas para âncoras internas da página
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');

            // Ignorar se for apenas # ou se for um link de navegação/ação
            if (href === '#' || href === '#home' || href === '#categorias' || href === '#salvos' || href === '#perfil') {
                return;
            }

            // Tentar encontrar o elemento alvo na página
            const target = document.querySelector(href);
            if (target) {
                e.preventDefault();
                
                const headerHeight = document.getElementById('cabecalho')?.offsetHeight || 0;
                const targetPosition = target.offsetTop - headerHeight;

                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
}

// ===================================================
// PERFIL E SALVOS
// ===================================================

function mostrarNoticiasSalvas() {
    // Criar modal ou navegar para página de salvos
    const salvos = window.JC.state.noticiasSalvas;

    if (salvos.length === 0) {
        mostrarMensagem('Nenhuma notícia salva', 'info');
        return;
    }

    // Implementar visualização de notícias salvas
    console.log('Notícias salvas:', salvos);
}

function mostrarPerfil() {
    // Criar modal de perfil
    const modal = criarModalPerfil();
    document.body.appendChild(modal);

    // Animar entrada
    requestAnimationFrame(() => {
        modal.classList.add('ativo');
    });
}

function criarModalPerfil() {
    const modal = document.createElement('div');
    modal.className = 'modal-perfil';
    modal.innerHTML = `
        <div class="modal-conteudo">
            <div class="modal-header">
                <h2>Meu Perfil</h2>
                <button class="modal-fechar">&times;</button>
            </div>
            <div class="modal-body">
                <div class="perfil-avatar">
                    <i class="fas fa-user-circle"></i>
                </div>
                <div class="perfil-opcoes">
                    <button class="botao-primario">Entrar</button>
                    <button class="botao-secundario">Criar conta</button>
                </div>
            </div>
        </div>
    `;

    // Fechar modal
    modal.querySelector('.modal-fechar').addEventListener('click', () => {
        modal.classList.remove('ativo');
        setTimeout(() => modal.remove(), 300);
    });

    // Fechar ao clicar fora
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.classList.remove('ativo');
            setTimeout(() => modal.remove(), 300);
        }
    });

    return modal;
}

// ===================================================
// MENSAGENS E NOTIFICAÇÕES
// ===================================================

function mostrarMensagem(texto, tipo = 'info') {
    const mensagem = document.createElement('div');
    mensagem.className = `mensagem-toast mensagem-${tipo}`;
    mensagem.textContent = texto;

    document.body.appendChild(mensagem);

    // Animar entrada
    requestAnimationFrame(() => {
        mensagem.classList.add('visivel');
    });

    // Remover após 3 segundos
    setTimeout(() => {
        mensagem.classList.remove('visivel');
        setTimeout(() => mensagem.remove(), 300);
    }, 3000);
}