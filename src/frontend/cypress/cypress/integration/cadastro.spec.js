describe('Testes de Cadastro', () => {
    beforeEach(() => {
      cy.visit('http://localhost:5500'); // Altere a URL conforme necessário
    });
  
    it('Deve preencher o formulário de cadastro e redirecionar para a tela de login', () => {
      cy.get('#cadastroForm').within(() => {
        cy.get('#nome').type('João da Silva');
        cy.get('#dataNascimento').type('2000-01-01');
        cy.get('#email').type('joao@example.com');
        cy.get('#senha').type('senhaSegura123');
        cy.get('input[type="submit"]').click();
      });
  
      // Verifica se a mensagem de erro está vazia
      cy.get('#mensagemErro').should('be.empty');
  
      // Verifica se foi redirecionado para a tela de login
      cy.get('#loginContainer').should('not.have.class', 'hidden');
      cy.get('#cadastroContainer').should('have.class', 'hidden');
    });
  
    it('Deve mostrar uma mensagem de erro se a idade for menor que 13 anos', () => {
      cy.get('#cadastroForm').within(() => {
        cy.get('#nome').type('Maria Sousa');
        cy.get('#dataNascimento').type('2015-01-01');
        cy.get('#email').type('maria@example.com');
        cy.get('#senha').type('senhaSegura123');
        cy.get('input[type="submit"]').click();
      });
  
      // Verifica se a mensagem de erro correta é exibida
      cy.get('#mensagemErro').should('contain', 'Você deve ter pelo menos 13 anos para se cadastrar.');
    });
  });
  