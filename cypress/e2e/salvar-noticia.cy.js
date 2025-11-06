describe('História 8 - Salvar Notícias para Ler Mais Tarde', () => {

  beforeEach(() => {
    cy.visit('/')
  })

  // Cenário 1: Notícia salva com sucesso
  it('Deve salvar uma notícia com sucesso quando o usuário está logado', () => {
    // Dado que o usuário está logado
    cy.login()

    // E está visualizando uma notícia de seu interesse
    cy.get('.cartao-noticia', { timeout: 10000 }).should('be.visible')
    cy.get('.cartao-noticia').first().click()
    cy.get('#botaoSalvar', { timeout: 10000 }).should('be.visible')

    // Quando ele clica no botão "Salvar"
    cy.get('#botaoSalvar').click()

    // Então a notícia deve ser adicionada à sua lista de "Ler mais tarde"
    // E o sistema deve exibir uma mensagem de confirmação
    cy.contains('Notícia salva com sucesso', { timeout: 5000 }).should('be.visible')
  })

  // Cenário 2: Acesso à lista de notícias salvas
  it('Deve visualizar uma lista com os títulos, imagens e links das notícias salvas', () => {
    // Dado que o usuário possui notícias salvas
    cy.login()

    // Salvar uma notícia primeiro
    cy.get('.cartao-noticia', { timeout: 10000 }).should('be.visible')
    cy.get('.cartao-noticia').first().click()
    cy.get('#botaoSalvar', { timeout: 10000 }).should('be.visible')
    cy.get('#botaoSalvar').click()
    cy.wait(1000)

    // Quando ele acessa a seção "Ler mais tarde"
    cy.acessarNoticiasSalvas()

    // Então ele deve visualizar uma lista com os títulos, imagens (se houver) e links das notícias salvas
    cy.get('.item-salvo').should('exist')
    cy.get('.item-salvo').should('have.length.greaterThan', 0)

    // Verificar elementos da notícia salva
    cy.get('.item-salvo').first().within(() => {
      cy.get('.item-salvo-titulo').should('exist')
      cy.get('a').should('have.attr', 'href')
      cy.get('.item-salvo-imagem').should('exist')
    })
  })

  // Cenário 3: Remover notícia salva
  it('Deve remover uma notícia da lista de salvos e confirmar a remoção', () => {
    // Dado que o usuário está na seção "Ler mais tarde"
    cy.login()

    // Salvar uma notícia primeiro
    cy.get('.cartao-noticia', { timeout: 10000 }).should('be.visible')
    cy.get('.cartao-noticia').first().click()
    cy.get('#botaoSalvar', { timeout: 10000 }).should('be.visible')
    cy.get('#botaoSalvar').click()
    cy.wait(1000)

    cy.acessarNoticiasSalvas()

    // E há uma notícia salva na lista
    cy.get('.item-salvo').should('exist')

    cy.get('.item-salvo').then(($noticias) => {
      const quantidadeAntes = $noticias.length

      // Quando ele clica na opção "Remover"
      cy.get('.item-salvo').first().within(() => {
        cy.get('.botao-remover').click()
      })

      // Então a notícia deve ser retirada da lista de salvos
      // E o sistema deve confirmar a remoção com uma mensagem adequada
      cy.contains('removida com sucesso', { timeout: 5000 }).should('be.visible')

      // Verificar se a lista diminuiu ou ficou vazia
      cy.get('body').then($body => {
        if ($body.find('.item-salvo').length > 0) {
          cy.get('.item-salvo').should('have.length', quantidadeAntes - 1)
        } else {
          cy.contains('Nenhuma notícia salva ainda').should('be.visible')
        }
      })
    })
  })

  // Cenário 4: Tentativa de salvar sem login
  it('Deve exibir mensagem solicitando login ao tentar salvar sem estar logado', () => {
    // Dado que o visitante não está logado
    // Quando ele tenta clicar no botão "Salvar"
    cy.get('.cartao-noticia', { timeout: 10000 }).should('be.visible')
    cy.get('.cartao-noticia').first().click()
    cy.get('#botaoSalvar', { timeout: 10000 }).should('be.visible')
    cy.get('#botaoSalvar').click()

    // Então o sistema deve exibir uma mensagem solicitando que ele faça login
    cy.contains(/faça login|fazer login|entre na sua conta/i, { timeout: 5000 }).should('be.visible')
  })
})
