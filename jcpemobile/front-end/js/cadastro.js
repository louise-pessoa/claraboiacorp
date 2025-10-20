/**
 * Modal de Cadastro de Usuário
 */

document.addEventListener('DOMContentLoaded', function() {
    const botaoPerfil = document.getElementById('botaoPerfil');
    const modalCadastro = document.getElementById('modalCadastro');
    const fecharModal = document.getElementById('fecharModalCadastro');
    const formCadastro = document.getElementById('formCadastro');
    const btnCadastrar = document.getElementById('btnCadastrar');
    const mensagemErro = document.getElementById('mensagemErro');
    const mensagemSucesso = document.getElementById('mensagemSucesso');
    
    if (botaoPerfil) {
        botaoPerfil.addEventListener('click', function(e) {
            e.preventDefault();
            abrirModal();
        });
    }
    
    if (fecharModal) {
        fecharModal.addEventListener('click', function(e) {
            e.preventDefault();
            fecharModalCadastro();
        });
    }
    
    if (modalCadastro) {
        modalCadastro.addEventListener('click', function(e) {
            if (e.target === modalCadastro) {
                fecharModalCadastro();
            }
        });
    }
    
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && modalCadastro.classList.contains('active')) {
            fecharModalCadastro();
        }
    });
    
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
    
    const inputs = formCadastro.querySelectorAll('.form-control');
    inputs.forEach(input => {
        input.addEventListener('input', function() {
            limparErro(this.name);
            this.classList.remove('error', 'shake');
        });
    });
    
    if (formCadastro) {
        formCadastro.addEventListener('submit', function(e) {
            e.preventDefault();
            submeterFormulario();
        });
    }
    
    function abrirModal() {
        modalCadastro.style.display = 'flex';
        setTimeout(() => {
            modalCadastro.classList.add('active');
        }, 10);
        document.body.style.overflow = 'hidden';
        
        const primeiroInput = formCadastro.querySelector('input');
        if (primeiroInput) {
            primeiroInput.focus();
        }
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
            nome: document.getElementById('id_nome').value.trim(),
            email: document.getElementById('id_email').value.trim(),
            senha: document.getElementById('id_senha').value,
            confirmar_senha: document.getElementById('id_confirmar_senha').value
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
        
        const nome = document.getElementById('id_nome').value.trim();
        if (!nome) {
            mostrarErroCampo('nome', 'O nome é obrigatório.');
            valido = false;
        }
        
        const email = document.getElementById('id_email').value.trim();
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!email) {
            mostrarErroCampo('email', 'O e-mail é obrigatório.');
            valido = false;
        } else if (!emailRegex.test(email)) {
            mostrarErroCampo('email', 'Digite um e-mail válido.');
            valido = false;
        }
        
        const senha = document.getElementById('id_senha').value;
        if (!senha) {
            mostrarErroCampo('senha', 'A senha é obrigatória.');
            valido = false;
        } else if (senha.length < 8) {
            mostrarErroCampo('senha', 'A senha deve ter no mínimo 8 caracteres.');
            valido = false;
        }
        
        const confirmarSenha = document.getElementById('id_confirmar_senha').value;
        if (!confirmarSenha) {
            mostrarErroCampo('confirmar_senha', 'A confirmação de senha é obrigatória.');
            valido = false;
        } else if (senha !== confirmarSenha) {
            mostrarErroCampo('confirmar_senha', 'As senhas não coincidem.');
            valido = false;
        }
        
        return valido;
    }
    
    function mostrarErroCampo(campo, mensagem) {
        const input = document.getElementById('id_' + campo);
        const erroSpan = document.getElementById('erro_' + campo);
        
        if (input) {
            input.classList.add('error', 'shake');
        }
        
        if (erroSpan) {
            erroSpan.textContent = mensagem;
        }
    }
    
    function limparErro(campo) {
        const erroSpan = document.getElementById('erro_' + campo);
        if (erroSpan) {
            erroSpan.textContent = '';
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
    
    function mostrarErros(errors) {
        for (const [campo, mensagem] of Object.entries(errors)) {
            if (campo === '__all__') {
                mostrarErroGeral(mensagem);
            } else {
                mostrarErroCampo(campo, mensagem);
            }
        }
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
