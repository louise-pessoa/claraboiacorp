/* ===================================================
   SWITCH TOGGLE VERSÃO CURTA - JORNAL DO COMMERCIO
   Controla a alternância para versão curta (estilo Apple)
   Por padrão: COMPLETA (switch desativado/esquerda)
   Ao ativar: CURTA (switch ativado/direita)

   GARANTIAS DE ESTADO INICIAL:
   1. HTML sem atributo 'checked'
   2. JavaScript força unchecked ao carregar
   3. CSS garante posição inicial
   4. DOMContentLoaded adiciona segurança extra
   =================================================== */

(function() {
    'use strict';

    // GARANTIA 1: Executar imediatamente e no DOMContentLoaded
    function inicializarSwitch() {
        // Elementos
        const toggleInput = document.getElementById('toggleVersao');
        const artigo = document.querySelector('.artigo-noticia');

        // Verifica se os elementos existem
        if (!toggleInput || !artigo) {
            return;
        }

        // ===================================================
        // GARANTIA 2: FORÇAR ESTADO INICIAL DESATIVADO
        // ===================================================
        function garantirEstadoInicial() {
            // Remover qualquer classe de versão curta
            artigo.classList.remove('versao-curta');

            // Forçar switch desativado
            toggleInput.checked = false;

            // Limpar atributo checked do DOM se existir
            toggleInput.removeAttribute('checked');

            console.log('✓ Switch inicializado: DESATIVADO (versão completa)');
        }

        // Executar garantia de estado inicial
        garantirEstadoInicial();

        // ===================================================
        // FUNÇÃO PARA ALTERNAR VERSÃO
        // ===================================================
        function toggleVersao() {
            if (toggleInput.checked) {
                // Ativar versão CURTA (switch marcado/direita)
                artigo.classList.add('versao-curta');

                // Scroll suave para o topo do artigo
                setTimeout(() => {
                    artigo.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }, 100);

                // Salvar preferência no localStorage
                localStorage.setItem('jc_versao_noticia', 'curta');

                console.log('→ Versão CURTA ativada');
            } else {
                // Ativar versão COMPLETA (switch desmarcado/esquerda)
                artigo.classList.remove('versao-curta');

                // Salvar preferência no localStorage
                localStorage.setItem('jc_versao_noticia', 'completa');

                console.log('→ Versão COMPLETA ativada');
            }

            atualizarAriaLabel();
        }

        // Event listener para o input
        toggleInput.addEventListener('change', toggleVersao);

        // ===================================================
        // VERIFICAR PREFERÊNCIA SALVA (OPCIONAL)
        // ===================================================
        // Comentado para SEMPRE iniciar desativado
        // Descomente se quiser lembrar a preferência do usuário

        /*
        const preferenciaSalva = localStorage.getItem('jc_versao_noticia');
        if (preferenciaSalva === 'curta') {
            // Se usuário prefere versão curta, ativar switch
            toggleInput.checked = true;
            artigo.classList.add('versao-curta');
        } else {
            // Padrão: versão completa (switch desativado)
            toggleInput.checked = false;
        }
        */

        // ===================================================
        // GARANTIA 3: REFORÇAR ESTADO DESATIVADO
        // ===================================================
        // Mesmo que localStorage tenha valor, forçar desativado
        if (toggleInput.checked) {
            toggleInput.checked = false;
            artigo.classList.remove('versao-curta');
            console.log('⚠ Corrigido: Switch estava marcado incorretamente');
        }

        // Atualizar aria-label do input
        function atualizarAriaLabel() {
            const label = toggleInput.checked
                ? 'Desativar versão curta e voltar para versão completa'
                : 'Ativar versão curta da notícia';
            toggleInput.setAttribute('aria-label', label);
        }

        // Inicializar aria-label
        atualizarAriaLabel();

        // ===================================================
        // GARANTIA 4: OBSERVADOR DE MUTAÇÕES
        // ===================================================
        // Observa se alguém tentar mudar o estado do switch externamente
        const observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                if (mutation.type === 'attributes' && mutation.attributeName === 'checked') {
                    // Se o atributo checked for adicionado de forma indevida, remover
                    if (toggleInput.hasAttribute('checked') && !toggleInput.checked) {
                        toggleInput.removeAttribute('checked');
                        console.log('⚠ Atributo "checked" removido automaticamente');
                    }
                }
            });
        });

        // Iniciar observador
        observer.observe(toggleInput, {
            attributes: true,
            attributeFilter: ['checked']
        });

        console.log('✓ Switch totalmente inicializado com todas as garantias');
    }

    // ===================================================
    // EXECUTAR IMEDIATAMENTE
    // ===================================================
    inicializarSwitch();

    // ===================================================
    // GARANTIA 5: EXECUTAR NOVAMENTE NO DOMCONTENTLOADED
    // ===================================================
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            console.log('→ DOMContentLoaded: Reforçando estado inicial');
            inicializarSwitch();
        });
    }

})();
