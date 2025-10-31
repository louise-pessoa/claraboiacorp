describe('Teste de Compartilhamento de Notícias', () => {
  it('Deve compartilhar uma notícia a partir do card hero na home', () => {
    // Visita a página inicial
    cy.visit('http://127.0.0.1:8000/')
    
    // Aguarda o card hero estar visível
    cy.get('article.hero').should('be.visible')
    
    // Clica no botão de compartilhar dentro das ações do hero
    cy.get('.hero-actions button[aria-label="Compartilhar"]').click()
  })
})
