/**
 * Modal de Feedback
 * Gerencia a abertura, fechamento e envio do formulário de feedback
 */

// Função para abrir o modal de feedback
function abrirModalFeedback() {
    const modal = document.getElementById('modalFeedback');
    if (modal) {
        modal.classList.add('ativo');
        document.body.style.overflow = 'hidden'; // Previne scroll da página
    }
}

// Função para fechar o modal de feedback
function fecharModalFeedback() {
    const modal = document.getElementById('modalFeedback');
    if (modal) {
        modal.classList.remove('ativo');
        document.body.style.overflow = ''; // Restaura scroll da página
        
        // Limpa o formulário
        const form = document.getElementById('formFeedback');
        if (form) {
            form.reset();
            atualizarContador();
        }
    }
}

// Função para atualizar o contador de caracteres
function atualizarContador() {
    const textarea = document.getElementById('comentario');
    const contador = document.querySelector('.contador-caracteres');
    
    if (textarea && contador) {
        const tamanho = textarea.value.length;
        contador.textContent = `${tamanho}/140`;
        
        // Muda cor quando próximo do limite
        if (tamanho > 120) {
            contador.style.color = 'var(--cor-primaria)';
        } else {
            contador.style.color = 'var(--cor-texto-quaternario)';
        }
    }
}

// Inicialização quando o DOM estiver carregado
document.addEventListener('DOMContentLoaded', function() {
    // Botão de fechar
    const btnFechar = document.getElementById('fecharModalFeedback');
    if (btnFechar) {
        btnFechar.addEventListener('click', fecharModalFeedback);
    }

    // Fechar ao clicar fora do modal
    const modal = document.getElementById('modalFeedback');
    if (modal) {
        modal.addEventListener('click', function(e) {
            if (e.target === modal) {
                fecharModalFeedback();
            }
        });
    }

    // Fechar com tecla ESC
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            const modal = document.getElementById('modalFeedback');
            if (modal && modal.classList.contains('ativo')) {
                fecharModalFeedback();
            }
        }
    });

    // Contador de caracteres
    const textarea = document.getElementById('comentario');
    if (textarea) {
        textarea.addEventListener('input', atualizarContador);
    }

    // Envio do formulário
    const form = document.getElementById('formFeedback');
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Pega os dados do formulário
            const satisfacao = document.querySelector('input[name="satisfacao"]:checked');
            const comentario = document.getElementById('comentario').value;
            
            if (!satisfacao) {
                alert('Por favor, selecione um nível de satisfação.');
                return;
            }
            
            // Dados do feedback
            const feedbackData = {
                satisfacao: satisfacao.value,
                comentario: comentario.trim()
            };
            
            console.log('Feedback enviado:', feedbackData);
            
            // Aqui você pode adicionar a chamada AJAX para enviar ao backend
            // Por enquanto, apenas mostra mensagem de sucesso
            
            alert('Obrigado pelo seu feedback! 🎉');
            fecharModalFeedback();
            
            // TODO: Implementar envio para o backend
            // enviarFeedbackParaBackend(feedbackData);
        });
    }
});

// Função para enviar feedback ao backend (a ser implementada)
function enviarFeedbackParaBackend(data) {
    // Exemplo de como seria a implementação com fetch
    /*
    fetch('/api/feedback/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        console.log('Feedback salvo:', data);
        alert('Obrigado pelo seu feedback! 🎉');
        fecharModalFeedback();
    })
    .catch(error => {
        console.error('Erro ao enviar feedback:', error);
        alert('Erro ao enviar feedback. Tente novamente.');
    });
    */
}

// Função auxiliar para pegar o CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
