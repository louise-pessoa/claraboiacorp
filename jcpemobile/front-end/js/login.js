/**
 * Modal de Login
 */

document.addEventListener('DOMContentLoaded', function() {
    const botaoPerfil = document.getElementById('botaoPerfil');
    const linkEntrarMenu = document.getElementById('linkEntrarMenu');
    const modalLogin = document.getElementById('modalLogin');
    const fecharModal = document.getElementById('fecharModalLogin');
    const formLogin = document.getElementById('formLogin');
    const btnEntrar = document.getElementById('btnEntrar');
    const mensagemErro = document.getElementById('mensagemErroLogin');
    const mensagemSucesso = document.getElementById('mensagemSucessoLogin');
    const linkCadastro = document.getElementById('linkCadastro');
    
    // Abrir modal ao clicar no ícone de perfil
    if (botaoPerfil) {
        botaoPerfil.addEventListener('click', function(e) {
            e.preventDefault();
            abrirModal();
        });
    }
    
    // Abrir modal ao clicar no link "Entrar" do menu lateral
    if (linkEntrarMenu) {
        linkEntrarMenu.addEventListener('click', function(e) {
            e.preventDefault();
            abrirModal();
            // Fechar menu lateral se estiver aberto
            const menuLateral = document.getElementById('menuLateral');
            if (menuLateral && menuLateral.classList.contains('active')) {
                menuLateral.classList.remove('active');
                const menuOverlay = document.getElementById('menuOverlay');
                if (menuOverlay) {
                    menuOverlay.classList.remove('active');
                }
            }
        });
    }
    
    // Fechar modal ao clicar no X
    if (fecharModal) {
        fecharModal.addEventListener('click', function(e) {
            e.preventDefault();
            fecharModalLogin();
        });
    }
    
    // Fechar modal ao clicar fora
    if (modalLogin) {
        modalLogin.addEventListener('click', function(e) {
            if (e.target === modalLogin) {
                fecharModalLogin();
            }
        });
    }
    
    // Fechar modal com ESC
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && modalLogin.classList.contains('active')) {
            fecharModalLogin();
        }
    });
    
    // Toggle de mostrar/ocultar senha
    const togglePasswordButtons = document.querySelectorAll('.toggle-password');
    togglePasswordButtons.forEach(button => {
        button.addEventListener('click', function() {
            const targetId = this.getAttribute('data-target');
            const input = document.getElementById(targetId);
            const icon = this.querySelector('i');
            
            if (input.type === 'password') {
                input.type = 'text';
                icon.classList.remove('fa-eye');
                icon.classList.add('fa-eye-slash');
            } else {
                input.type = 'password';
                icon.classList.remove('fa-eye-slash');
                icon.classList.add('fa-eye');
            }
        });
    });
    
    // Limpar erros ao digitar
    const inputs = formLogin.querySelectorAll('.form-control');
    inputs.forEach(input => {
        input.addEventListener('input', function() {
            this.classList.remove('error', 'shake');
            const errorSpan = document.getElementById('erro_' + this.id);
            if (errorSpan) {
                errorSpan.textContent = '';
            }
        });
    });
    
    // Link para abrir modal de cadastro
    if (linkCadastro) {
        linkCadastro.addEventListener('click', function(e) {
            e.preventDefault();
            fecharModalLogin();
            // Abrir modal de cadastro
            if (typeof window.abrirModalCadastro === 'function') {
                window.abrirModalCadastro();
            }
        });
    }
    
    // Submit do formulário
    if (formLogin) {
        formLogin.addEventListener('submit', function(e) {
            e.preventDefault();
            submeterFormulario();
        });
    }
    
    function abrirModal() {
        modalLogin.style.display = 'flex';
        setTimeout(() => {
            modalLogin.classList.add('active');
        }, 10);
        document.body.style.overflow = 'hidden';
        
        // Focar no primeiro input
        const primeiroInput = formLogin.querySelector('input');
        if (primeiroInput) {
            primeiroInput.focus();
        }
    }
    
    function fecharModalLogin() {
        modalLogin.classList.remove('active');
        setTimeout(() => {
            modalLogin.style.display = 'none';
            limparFormulario();
        }, 300);
        document.body.style.overflow = '';
    }
    
    function limparFormulario() {
        formLogin.reset();
        esconderMensagens();
        limparTodosErros();
    }
    
    function submeterFormulario() {
        esconderMensagens();
        limparTodosErros();
        
        if (!validarFormulario()) {
            return;
        }
        
        btnEntrar.disabled = true;
        btnEntrar.classList.add('loading');
        
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        
        const formData = new FormData();
        formData.append('email', document.getElementById('login_email').value.trim());
        formData.append('senha', document.getElementById('login_senha').value);
        formData.append('csrfmiddlewaretoken', csrftoken);
        
        fetch('/login/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                mostrarSucesso(data.message);
                setTimeout(() => {
                    window.location.href = data.redirect_url || '/';
                }, 1000);
            } else {
                mostrarErroGeral(data.message || 'E-mail ou senha incorretos.');
                btnEntrar.disabled = false;
                btnEntrar.classList.remove('loading');
            }
        })
        .catch(error => {
            console.error('Erro:', error);
            mostrarErroGeral('Erro ao processar login. Tente novamente.');
            btnEntrar.disabled = false;
            btnEntrar.classList.remove('loading');
        });
    }
    
    function validarFormulario() {
        let valido = true;
        
        const email = document.getElementById('login_email').value.trim();
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!email) {
            mostrarErroCampo('login_email', 'O e-mail é obrigatório.');
            valido = false;
        } else if (!emailRegex.test(email)) {
            mostrarErroCampo('login_email', 'Digite um e-mail válido.');
            valido = false;
        }
        
        const senha = document.getElementById('login_senha').value;
        if (!senha) {
            mostrarErroCampo('login_senha', 'A senha é obrigatória.');
            valido = false;
        }
        
        return valido;
    }
    
    function mostrarErroCampo(campoId, mensagem) {
        const input = document.getElementById(campoId);
        const erroSpan = document.getElementById('erro_' + campoId);
        
        if (input) {
            input.classList.add('error', 'shake');
        }
        
        if (erroSpan) {
            erroSpan.textContent = mensagem;
        }
    }
    
    function limparTodosErros() {
        const erroSpans = document.querySelectorAll('.form-error');
        erroSpans.forEach(span => {
            span.textContent = '';
        });
        
        const inputs = document.querySelectorAll('.form-control');
        inputs.forEach(input => {
            input.classList.remove('error', 'shake');
        });
    }
    
    function mostrarErroGeral(mensagem) {
        mensagemErro.textContent = mensagem;
        mensagemErro.style.display = 'block';
        
        const modalBody = document.querySelector('.modal-body');
        if (modalBody) {
            modalBody.scrollTop = 0;
        }
    }
    
    function mostrarSucesso(mensagem) {
        mensagemSucesso.textContent = mensagem;
        mensagemSucesso.style.display = 'block';
        
        const modalBody = document.querySelector('.modal-body');
        if (modalBody) {
            modalBody.scrollTop = 0;
        }
    }
    
    function esconderMensagens() {
        mensagemErro.style.display = 'none';
        mensagemSucesso.style.display = 'none';
    }
});
