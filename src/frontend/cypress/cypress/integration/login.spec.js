describe('Testes de Login', () => {
    beforeEach(() => {
        cy.visit('http://localhost:5500'); // Altere a URL conforme necessário

        // Supondo que primeiro precisamos ir para a tela de login após o cadastro
        cy.get('#cadastroForm').within(() => {
            cy.get('#nome').type('João da Silva');
            cy.get('#dataNascimento').type('2000-01-01');
            cy.get('#email').type('joao@example.com');
            cy.get('#senha').type('senhaSegura123');
            cy.get('input[type="submit"]').click();
        });

        // Aguardar redirecionamento para a tela de login
        cy.get('#loginContainer').should('not.have.class', 'hidden');
    });

    it('Deve fazer login com sucesso e redirecionar para a tela de notícias', () => {
        cy.get('#loginForm').within(() => {
            cy.get('#loginEmail').type('joao@example.com');

            // Verifica se o campo de senha está habilitado antes de digitar
            cy.get('#loginSenha').should('not.be.disabled').type('senhaSegura123');

            cy.get('input[type="submit"]').click();
        });

        // Verifica se foi redirecionado para a tela de notícias
        cy.get('#noticiasContainer').should('not.have.class', 'hidden');
        cy.get('#loginContainer').should('have.class', 'hidden');
    });

    it('Deve mostrar uma mensagem de erro para credenciais inválidas', () => {
        cy.get('#loginForm').within(() => {
            cy.get('#loginEmail').type('usuarioInvalido@example.com');

            // Verifica se o campo de senha está habilitado antes de digitar
            cy.get('#loginSenha').should('not.be.disabled').type('senhaErrada');

            cy.get('input[type="submit"]').click();
        });

        // Verifica se a mensagem de erro correta é exibida
        cy.get('#loginErro').should('contain', 'Credenciais inválidas. Tente novamente.');

        // Verifica se a tela de login ainda está visível (não redirecionou)
        cy.get('#loginContainer').should('not.have.class', 'hidden');
        cy.get('#noticiasContainer').should('have.class', 'hidden');
    });
});
