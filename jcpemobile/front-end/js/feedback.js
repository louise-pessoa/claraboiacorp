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

        // Limpa preview de imagem
        const inputImagem = document.getElementById('imagemFeedback');
        const imagemPreview = document.getElementById('imagemPreview');
        const previewContainer = document.getElementById('previewContainer');
        const nomeArquivo = document.getElementById('nomeArquivo');
        const btnSelecionarImagem = document.getElementById('btnSelecionarImagem');

        if (inputImagem) inputImagem.value = '';
        if (imagemPreview) imagemPreview.src = '';
        if (previewContainer) previewContainer.style.display = 'none';
        if (nomeArquivo) nomeArquivo.textContent = '';
        if (btnSelecionarImagem) btnSelecionarImagem.style.display = 'inline-block';
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

    // Gerenciamento de upload de imagem
    const btnSelecionarImagem = document.getElementById('btnSelecionarImagem');
    const inputImagem = document.getElementById('imagemFeedback');
    const previewContainer = document.getElementById('previewContainer');
    const imagemPreview = document.getElementById('imagemPreview');
    const btnRemoverImagem = document.getElementById('btnRemoverImagem');
    const nomeArquivo = document.getElementById('nomeArquivo');

    // Abrir seletor de arquivo ao clicar no botão
    if (btnSelecionarImagem && inputImagem) {
        btnSelecionarImagem.addEventListener('click', function() {
            inputImagem.click();
        });
    }

    // Preview da imagem selecionada
    if (inputImagem) {
        inputImagem.addEventListener('change', function(e) {
            const arquivo = e.target.files[0];

            if (arquivo) {
                // Validar tamanho do arquivo (max 5MB)
                if (arquivo.size > 5 * 1024 * 1024) {
                    alert('A imagem deve ter no máximo 5MB.');
                    inputImagem.value = '';
                    return;
                }

                // Validar tipo de arquivo
                if (!arquivo.type.startsWith('image/')) {
                    alert('Por favor, selecione apenas arquivos de imagem.');
                    inputImagem.value = '';
                    return;
                }

                // Mostrar preview
                const reader = new FileReader();
                reader.onload = function(e) {
                    imagemPreview.src = e.target.result;
                    previewContainer.style.display = 'block';
                    nomeArquivo.textContent = arquivo.name;
                    btnSelecionarImagem.style.display = 'none';
                };
                reader.readAsDataURL(arquivo);
            }
        });
    }

    // Remover imagem
    if (btnRemoverImagem) {
        btnRemoverImagem.addEventListener('click', function() {
            inputImagem.value = '';
            imagemPreview.src = '';
            previewContainer.style.display = 'none';
            nomeArquivo.textContent = '';
            btnSelecionarImagem.style.display = 'inline-block';
        });
    }

    // Envio do formulário
    const form = document.getElementById('formFeedback');
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();

            // Pega os dados do formulário
            const satisfacao = document.querySelector('input[name="satisfacao"]:checked');
            const comentario = document.getElementById('comentario').value;
            const imagemInput = document.getElementById('imagemFeedback');

            if (!satisfacao) {
                alert('Por favor, selecione um nível de satisfação.');
                return;
            }

            // Cria FormData para enviar arquivo
            const formData = new FormData();
            formData.append('avaliacao', satisfacao.value);
            formData.append('comentario', comentario.trim());
            formData.append('nome', 'Anônimo');  // Por enquanto, pode ser anônimo
            formData.append('email', 'feedback@claraboia.com');  // Email padrão

            // Adiciona imagem se houver
            if (imagemInput.files.length > 0) {
                formData.append('imagem', imagemInput.files[0]);
            }

            console.log('Feedback enviado');

            // Envia para o backend
            enviarFeedbackParaBackend(formData);
        });
    }
});

// Função para enviar feedback ao backend
function enviarFeedbackParaBackend(formData) {
    // Desabilita o botão de envio para evitar múltiplos cliques
    const btnEnviar = document.querySelector('.btn-enviar-feedback');
    if (btnEnviar) {
        btnEnviar.disabled = true;
        btnEnviar.textContent = 'Enviando...';
    }

    // Quando enviamos FormData, NÃO devemos definir Content-Type
    // O navegador define automaticamente com o boundary correto
    fetch('/feedback/enviar/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'X-Requested-With': 'XMLHttpRequest'
        },
        body: formData
    })
    .then(response => response.json())
    .then(result => {
        if (result.success) {
            console.log('Feedback salvo com sucesso:', result);
            alert(result.message || 'Obrigado pelo seu feedback!');
            fecharModalFeedback();
        } else {
            console.error('Erro ao salvar feedback:', result);
            alert(result.message || 'Erro ao enviar feedback. Tente novamente.');
        }
    })
    .catch(error => {
        console.error('Erro ao enviar feedback:', error);
        alert('Erro ao enviar feedback. Por favor, tente novamente.');
    })
    .finally(() => {
        // Reabilita o botão de envio
        if (btnEnviar) {
            btnEnviar.disabled = false;
            btnEnviar.textContent = 'Enviar avaliação';
        }
    });
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
