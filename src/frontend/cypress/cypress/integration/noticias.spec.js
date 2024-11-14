describe('Testes de Notícias', () => {
    beforeEach(() => {
      cy.visit('http://localhost:5500'); // Altere a URL conforme necessário
  
      // Prepara o estado inicial cadastrando e logando um usuário
      cy.get('#cadastroContainer').within(() => {
        cy.get('#nome').type('João da Silva');
        cy.get('#dataNascimento').type('2000-01-01');
        cy.get('#email').type('joao@example.com');
        cy.get('#senha').type('senhaSegura123');
        cy.get('input[type="submit"]').click(); // Botão de envio no formulário de cadastro
      });
  
      cy.get('#loginContainer').within(() => {
        cy.get('#loginEmail').type('joao@example.com');
        cy.get('#loginSenha').type('senhaSegura123');
        cy.get('input[type="submit"]').click(); // Botão de envio no formulário de login
      });
    });
  
    it('Deve exibir as notícias mockadas corretamente', () => {
      cy.get('#noticiasContainer').should('not.have.class', 'hidden');
  
      // Verifica se as notícias mockadas são exibidas
      cy.get('.news-item').should('have.length', 4);
      cy.get('.news-title').first().should('contain', 'Vitória Impressionante');
      cy.get('.news-content').first().should('contain', 'O time conquistou uma vitória impressionante ontem.');
    });
  });
  