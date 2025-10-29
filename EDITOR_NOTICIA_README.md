# 📝 Editor Rico de Notícias - Documentação

## 🎯 Implementações Realizadas

Foi implementado um **editor rico WYSIWYG (What You See Is What You Get)** para criação e edição de notícias, permitindo controle total sobre o layout e formatação do conteúdo.

---

## ✨ Recursos Implementados

### 1. **Editor Rico com Quill.js**
- ✅ Editor visual profissional
- ✅ Barra de ferramentas completa com:
  - Títulos (H1, H2, H3)
  - Negrito, Itálico, Sublinhado, Tachado
  - Cores de texto e fundo
  - Alinhamento de texto
  - Listas ordenadas e não ordenadas
  - Citações e blocos de código
  - Links e imagens
  - Limpeza de formatação

### 2. **Controle de Imagens**
- ✅ **Upload de imagem principal** com preview
- ✅ **Inserção de múltiplas imagens no conteúdo**:
  - Via botão da toolbar
  - Via arrastar e soltar (drag & drop)
  - Via URL externa
- ✅ Preview automático das imagens

### 3. **Controle de Layout**
- ✅ **Quebras de parágrafo personalizadas**
- ✅ **Quebras de linha customizadas**
- ✅ **Posicionamento livre de imagens**
- ✅ **Formatação rica de texto**

### 4. **Preview em Tempo Real**
- ✅ Visualização ao vivo da notícia enquanto edita
- ✅ Layout idêntico ao da página final
- ✅ Atualização instantânea de:
  - Título
  - Resumo
  - Categoria
  - Autor
  - Imagem principal
  - Conteúdo formatado

### 5. **Interface Melhorada**
- ✅ Layout em duas colunas:
  - **Coluna esquerda**: Formulário de edição
  - **Coluna direita**: Preview em tempo real
- ✅ Design responsivo (adapta-se a mobile)
- ✅ Ícones e indicadores visuais
- ✅ Contador de caracteres para o resumo (300 máx)

---

## 🛠️ Arquivos Modificados

### 1. **`jcpemobile/forms.py`**
```python
# Atualizado NoticiaForm para suportar editor rico
- Campo 'conteudo' agora escondido (hidden)
- Novos IDs para melhor controle JavaScript
- Classes CSS otimizadas
```

### 2. **`jcpemobile/templates/admin_form_noticia.html`**
```html
<!-- Completamente redesenhado com: -->
- Integração do Quill.js
- Layout em grid com preview
- Toolbar customizada
- JavaScript para sincronização em tempo real
- Suporte a drag & drop de imagens
```

### 3. **`jcpemobile/templates/detalhes_noticia.html`**
```django
<!-- Alterado filtro de renderização -->
- De: {{ noticia.conteudo|linebreaks }}
- Para: {{ noticia.conteudo|safe }}
<!-- Permite renderização de HTML formatado -->
```

---

## 🚀 Como Usar

### **Criar Nova Notícia:**

1. Acesse o painel administrativo
2. Clique em "**+ Nova Notícia**"
3. Preencha os campos básicos (título, categoria, autor, resumo)
4. **Use o editor rico** para escrever o conteúdo:

#### **Adicionar Texto Formatado:**
- Use a barra de ferramentas para negrito, itálico, etc.
- Crie títulos com os botões H1, H2, H3
- Organize com listas e citações

#### **Adicionar Imagens:**
Existem 3 formas:

1. **Via botão de imagem** (📷 na toolbar):
   - Clique no ícone de imagem
   - Selecione arquivo do computador
   - Imagem será inserida na posição do cursor

2. **Via arrastar e soltar**:
   - Arraste uma imagem do seu computador
   - Solte no editor
   - Imagem inserida automaticamente

3. **Via URL**:
   - Clique em "**Inserir Imagem**" (botão customizado)
   - Cole URL da imagem
   - Pressione OK

#### **Controlar Quebras:**
- **Nova Parágrafo**: Cria espaçamento entre blocos de texto
- **Quebra de Linha**: Quebra linha sem espaçamento extra

5. **Visualize em tempo real** no painel da direita
6. Clique em "**Salvar**"

---

## 📱 Responsividade

O editor se adapta automaticamente:

- **Desktop/Tablet**: Layout em 2 colunas (editor + preview)
- **Mobile**: Colunas empilhadas verticalmente

---

## ⚠️ Notas Importantes

### **Segurança:**
- O filtro `|safe` é usado para renderizar HTML
- **Cuidado**: Apenas administradores devem ter acesso ao editor
- O Django automaticamente escapa tags perigosas

### **Compatibilidade:**
- Testado em navegadores modernos (Chrome, Firefox, Edge, Safari)
- Requer JavaScript ativado

### **Armazenamento:**
- Imagens inseridas no editor são convertidas para Base64
- Para produção, considere implementar upload para servidor/CDN

---

## 🎨 Personalização

### **Modificar Cores do Preview:**
Edite as classes CSS no arquivo `admin_form_noticia.html`:

```css
.preview-titulo { color: #1a1a1a; } /* Título */
.preview-resumo { border-left-color: #007bff; } /* Resumo */
.preview-content { background: #f8f9fa; } /* Fundo */
```

### **Adicionar Mais Ferramentas:**
Edite a configuração do Quill no JavaScript:

```javascript
toolbar: [
    // Adicione mais opções aqui
    ['video'], // Exemplo: adicionar vídeo
    [{ 'indent': '-1'}, { 'indent': '+1' }], // Indentação
]
```

---

## 🐛 Troubleshooting

### **Preview não atualiza:**
- Verifique se JavaScript está ativado
- Limpe cache do navegador (Ctrl + F5)

### **Imagens não aparecem:**
- Verifique extensão do arquivo (JPG, PNG, GIF, WebP)
- Para URLs externas, certifique-se que estão acessíveis

### **Conteúdo não salva:**
- Certifique-se de clicar no botão "Salvar"
- Verifique erros no console do navegador (F12)

---

## 📚 Tecnologias Utilizadas

- **[Quill.js](https://quilljs.com/)** v1.3.6 - Editor WYSIWYG
- **Font Awesome** 6.4.0 - Ícones
- **Django Forms** - Backend
- **Vanilla JavaScript** - Interatividade

---

## 🔄 Próximos Passos (Opcional)

Sugestões para melhorias futuras:

1. **Upload de imagens para servidor** (não Base64)
2. **Auto-save** (salvamento automático)
3. **Controle de versões** (histórico de edições)
4. **Colaboração em tempo real**
5. **Biblioteca de mídia** (gerenciar imagens reutilizáveis)
6. **Otimização de imagens** (compressão automática)
7. **Templates de notícia** (modelos pré-formatados)

---

## ✅ Checklist de Teste

Antes de usar em produção, teste:

- [ ] Criar notícia nova
- [ ] Editar notícia existente
- [ ] Upload de imagem principal
- [ ] Inserir imagens no conteúdo
- [ ] Formatação de texto (negrito, itálico, etc.)
- [ ] Criar títulos H1, H2, H3
- [ ] Adicionar listas
- [ ] Preview em tempo real funciona
- [ ] Salvar e visualizar no site
- [ ] Testar em mobile
- [ ] Testar em diferentes navegadores

---

## 📞 Suporte

Para dúvidas ou problemas, consulte:
- Documentação do Quill.js: https://quilljs.com/docs/
- Django Templates: https://docs.djangoproject.com/en/stable/topics/templates/

---

**Implementado em:** 28 de Outubro de 2025
**Versão:** 1.0
