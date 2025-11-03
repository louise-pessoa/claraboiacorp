// ***********************************************
// This example commands.js shows you how to
// create various custom commands and overwrite
// existing commands.
//
// For more comprehensive examples of custom
// commands please read more here:
// https://on.cypress.io/custom-commands
// ***********************************************

// Comando customizado para login
Cypress.Commands.add('login', (email, password) => {
  // Usar credenciais passadas como parâmetro ou buscar do ambiente
  const userEmail = email || Cypress.env('TEST_USER_EMAIL')
  const userPassword = password || Cypress.env('TEST_USER_PASSWORD')
  
  // Validar se as credenciais existem
  if (!userEmail || !userPassword) {
    throw new Error('Credenciais não configuradas! Verifique o arquivo cypress.env.json')
  }
  
  cy.get('#menuHamburguer').click()
  cy.get('#linkEntrarMenu').click()
  cy.get('#login_email').type(userEmail)
  cy.get('#login_senha').type(userPassword)
  cy.get('#btnEntrar').click()
  
  // Aguardar o modal fechar completamente
  cy.get('#modalLogin', { timeout: 5000 }).should('not.be.visible')
  
  // Verificar se está na home page
  cy.url().should('eq', Cypress.config().baseUrl + '/')
  
  // Aguardar a página carregar completamente
  cy.wait(500)
})

// Comando customizado para acessar notícias salvas
Cypress.Commands.add('acessarNoticiasSalvas', () => {
  cy.get('#menuHamburguer').click()
  cy.contains('Notícias Salvas').click()
})

//
// -- This is a child command --
// Cypress.Commands.add('drag', { prevSubject: 'element'}, (subject, options) => { ... })
//
//
// -- This is a dual command --
// Cypress.Commands.add('dismiss', { prevSubject: 'optional'}, (subject, options) => { ... })
//
//
// -- This will overwrite an existing command --
// Cypress.Commands.overwrite('visit', (originalFn, url, options) => { ... })