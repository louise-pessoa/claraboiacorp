/**
 * Modal de Cadastro
 */

document.addEventListener('DOMContentLoaded', function() {
    const modalCadastro = document.getElementById('modalCadastro');
    const fecharModal = document.getElementById('fecharModalCadastro');
    const formCadastro = document.getElementById('formCadastro');
    const btnCadastrar = document.getElementById('btnCadastrar');
    const mensagemErro = document.getElementById('mensagemErroCadastro');
    const mensagemSucesso = document.getElementById('mensagemSucessoCadastro');
    const linkLogin = document.getElementById('linkLogin');
    
    // Fechar modal ao clicar no X
    if (fecharModal) {
        fecharModal.addEventListener('click', function(e) {
            e.preventDefault();
            fecharModalCadastro();
        });
    }
    
    // Fechar modal ao clicar fora
    if (modalCadastro) {
        modalCadastro.addEventListener('click', function(e) {
            if (e.target === modalCadastro) {
                fecharModalCadastro();
            }
        });
    }
    
    // Fechar modal com ESC
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && modalCadastro.classList.contains('active')) {
            fecharModalCadastro();
        }
    });
    
    // Toggle de mostrar/ocultar senha
    const togglePasswordButtons = document.querySelectorAll('#modalCadastro .toggle-password');
    togglePasswordButtons.forEach(button => {
        button.addEventListener('click', function() {
            const targetId = this.getAttribute('data-target');
            const input = document.getElementById(targetId);
            const icon = this.querySelector('i');
            
            if (input && input.type === 'password') {
                input.type = 'text';
                icon.classList.remove('fa-eye');
                icon.classList.add('fa-eye-slash');
            } else if (input) {
                input.type = 'password';
                icon.classList.remove('fa-eye-slash');
                icon.classList.add('fa-eye');
            }
        });
    });
    
    // Limpar erros ao digitar
    const inputs = formCadastro.querySelectorAll('.form-control');
    inputs.forEach(input => {
        input.addEventListener('input', function() {
            this.classList.remove('error', 'shake');
            const errorSpan = document.getElementById('erro_' + this.id);
            if (errorSpan) {
                errorSpan.textContent = '';
            }
        });
    });
    
    // Link para abrir modal de login
    if (linkLogin) {
        linkLogin.addEventListener('click', function(e) {
            e.preventDefault();
            fecharModalCadastro();
            // Abrir modal de login
            const modalLogin = document.getElementById('modalLogin');
            if (modalLogin) {
                modalLogin.style.display = 'flex';
                setTimeout(() => {
                    modalLogin.classList.add('active');
                }, 10);
            }
        });
    }
    
    // Submit do formulário
    if (formCadastro) {
        formCadastro.addEventListener('submit', function(e) {
            e.preventDefault();
            submeterFormulario();
        });
    }
    
    function fecharModalCadastro() {
        modalCadastro.classList.remove('active');
        setTimeout(() => {
            modalCadastro.style.display = 'none';
            limparFormulario();
        }, 300);
        document.body.style.overflow = '';
    }
    
    function limparFormulario() {
        formCadastro.reset();
        esconderMensagens();
        limparTodosErros();
    }
    
    function submeterFormulario() {
        esconderMensagens();
        limparTodosErros();
        
        if (!validarFormulario()) {
            return;
        }
        
        btnCadastrar.disabled = true;
        btnCadastrar.classList.add('loading');
        
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        
        const formData = {
            nome: document.getElementById('cadastro_nome').value.trim(),
            email: document.getElementById('cadastro_email').value.trim(),
            senha: document.getElementById('cadastro_senha').value,
            confirmar_senha: document.getElementById('cadastro_confirmar_senha').value
        };
        
        fetch('/cadastro/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: JSON.stringify(formData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                mostrarSucesso(data.message);
                setTimeout(() => {
                    window.location.href = data.redirect_url || '/';
                }, 1500);
            } else {
                mostrarErros(data.errors);
                btnCadastrar.disabled = false;
                btnCadastrar.classList.remove('loading');
            }
        })
        .catch(error => {
            console.error('Erro:', error);
            mostrarErroGeral('Erro ao processar cadastro. Tente novamente.');
            btnCadastrar.disabled = false;
            btnCadastrar.classList.remove('loading');
        });
    }
    
    function validarFormulario() {
        let valido = true;
        
        const nome = document.getElementById('cadastro_nome').value.trim();
        if (!nome) {
            mostrarErroCampo('cadastro_nome', 'O nome é obrigatório.');
            valido = false;
        }
        
        const email = document.getElementById('cadastro_email').value.trim();
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!email) {
            mostrarErroCampo('cadastro_email', 'O e-mail é obrigatório.');
            valido = false;
        } else if (!emailRegex.test(email)) {
            mostrarErroCampo('cadastro_email', 'Digite um e-mail válido.');
            valido = false;
        }
        
        const senha = document.getElementById('cadastro_senha').value;
        if (!senha) {
            mostrarErroCampo('cadastro_senha', 'A senha é obrigatória.');
            valido = false;
        } else if (senha.length < 8) {
            mostrarErroCampo('cadastro_senha', 'A senha deve ter no mínimo 8 caracteres.');
            valido = false;
        }
        
        const confirmarSenha = document.getElementById('cadastro_confirmar_senha').value;
        if (!confirmarSenha) {
            mostrarErroCampo('cadastro_confirmar_senha', 'A confirmação de senha é obrigatória.');
            valido = false;
        } else if (senha !== confirmarSenha) {
            mostrarErroCampo('cadastro_confirmar_senha', 'As senhas não coincidem.');
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
        const erroSpans = document.querySelectorAll('#modalCadastro .form-error');
        erroSpans.forEach(span => {
            span.textContent = '';
        });
        
        const inputs = document.querySelectorAll('#modalCadastro .form-control');
        inputs.forEach(input => {
            input.classList.remove('error', 'shake');
        });
    }
    
    function mostrarErros(errors) {
        for (const [campo, mensagem] of Object.entries(errors)) {
            if (campo === '__all__') {
                mostrarErroGeral(mensagem);
            } else {
                mostrarErroCampo('cadastro_' + campo, mensagem);
            }
        }
    }
    
    function mostrarErroGeral(mensagem) {
        mensagemErro.textContent = mensagem;
        mensagemErro.style.display = 'block';
        
        const modalBody = document.querySelector('#modalCadastro .modal-body');
        if (modalBody) {
            modalBody.scrollTop = 0;
        }
    }
    
    function mostrarSucesso(mensagem) {
        mensagemSucesso.textContent = mensagem;
        mensagemSucesso.style.display = 'block';
        
        const modalBody = document.querySelector('#modalCadastro .modal-body');
        if (modalBody) {
            modalBody.scrollTop = 0;
        }
    }
    
    function esconderMensagens() {
        mensagemErro.style.display = 'none';
        mensagemSucesso.style.display = 'none';
    }
    
    // Função global para abrir o modal de cadastro (pode ser chamada de outros lugares)
    window.abrirModalCadastro = function() {
        modalCadastro.style.display = 'flex';
        setTimeout(() => {
            modalCadastro.classList.add('active');
        }, 10);
        document.body.style.overflow = 'hidden';
        
        const primeiroInput = formCadastro.querySelector('input');
        if (primeiroInput) {
            primeiroInput.focus();
        }
    };
});

