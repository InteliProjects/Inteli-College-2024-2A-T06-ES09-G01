package main

import (
	"bytes"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"
)

// Testa o loginHandler para requisições POST válidas
func TestLoginHandler_Success(t *testing.T) {
	req, err := http.NewRequest("POST", "/login", bytes.NewBufferString(`{"username":"testuser","password":"testpass"}`))
	if err != nil {
		t.Fatal(err)
	}
	rr := httptest.NewRecorder()
	handler := http.HandlerFunc(loginHandler)

	handler.ServeHTTP(rr, req)

	// Verifica se o status retornado é OK (200)
	if status := rr.Code; status != http.StatusOK {
		t.Errorf("Expected status code %d but got %d", http.StatusOK, status)
	}

	expected := `{"message":"Login successful"}`
	actual := strings.TrimSpace(rr.Body.String())

	// Compara o corpo da resposta com o esperado
	if actual != expected {
		t.Errorf("Expected body %s but got %s", expected, actual)
	}
}

// Testa o loginHandler para requisições POST com dados inválidos
func TestLoginHandler_InvalidRequest(t *testing.T) {
	req, err := http.NewRequest("POST", "/login", bytes.NewBufferString(`{"username":"","password":""}`))
	if err != nil {
		t.Fatal(err)
	}
	rr := httptest.NewRecorder()
	handler := http.HandlerFunc(loginHandler)

	handler.ServeHTTP(rr, req)

	// Verifica se o status retornado é Unauthorized (401)
	if status := rr.Code; status != http.StatusUnauthorized {
		t.Errorf("Expected status code %d but got %d", http.StatusUnauthorized, status)
	}

	expected := "Unauthorized"
	actual := strings.TrimSpace(rr.Body.String())

	// Compara o corpo da resposta com o esperado
	if actual != expected {
		t.Errorf("Expected body %s but got %s", expected, actual)
	}
}

// Testa o loginHandler para métodos não suportados
func TestLoginHandler_MethodNotAllowed(t *testing.T) {
	req, err := http.NewRequest("GET", "/login", nil)
	if err != nil {
		t.Fatal(err)
	}
	rr := httptest.NewRecorder()
	handler := http.HandlerFunc(loginHandler)

	handler.ServeHTTP(rr, req)

	// Verifica se o status retornado é MethodNotAllowed (405)
	if status := rr.Code; status != http.StatusMethodNotAllowed {
		t.Errorf("Expected status code %d but got %d", http.StatusMethodNotAllowed, status)
	}

	expected := "Method not allowed"
	actual := strings.TrimSpace(rr.Body.String())

	// Compara o corpo da resposta com o esperado
	if actual != expected {
		t.Errorf("Expected body %s but got %s", expected, actual)
	}
}
