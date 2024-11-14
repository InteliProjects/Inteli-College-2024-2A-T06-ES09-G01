package main

import (
	"encoding/json"
	"net/http"
	"time"
)

// Estrutura para armazenar os dados de login enviados na requisição
// O payload de login será um JSON com os campos "username" e "password"
type LoginRequest struct {
	Username string `json:"username"` // Nome de usuário
	Password string `json:"password"` // Senha do usuário
}

// Estrutura para a resposta do login
// A resposta será um JSON com uma mensagem informando o sucesso ou falha no login
type LoginResponse struct {
	Message string `json:"message"` // Mensagem de resposta
}

// Função que lida com a requisição de login
// Ela verifica o método HTTP, decodifica o JSON de entrada, valida os dados e responde com sucesso ou erro
func loginHandler(w http.ResponseWriter, r *http.Request) {
	// Simula um tempo de resposta para o processamento da requisição (latência de 100ms)
	time.Sleep(100 * time.Millisecond)

	// Verifica se o método da requisição é POST. Se não for, retorna um erro "Method Not Allowed"
	if r.Method != http.MethodPost {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	// Cria uma instância de LoginRequest para armazenar os dados enviados na requisição
	var loginRequest LoginRequest
	// Decodifica o corpo da requisição (JSON) e armazena na estrutura LoginRequest
	err := json.NewDecoder(r.Body).Decode(&loginRequest)
	if err != nil {
		// Retorna um erro 400 (Bad Request) se a decodificação falhar
		http.Error(w, "Bad request", http.StatusBadRequest)
		return
	}

	// Aqui você pode adicionar sua lógica de autenticação (verificação no banco de dados, etc.)
	// No exemplo, simulamos um login bem-sucedido se username e password não estiverem vazios
	if loginRequest.Username != "" && loginRequest.Password != "" {
		// Retorna um status 200 (OK) e uma mensagem de sucesso
		w.WriteHeader(http.StatusOK)
		json.NewEncoder(w).Encode(LoginResponse{Message: "Login successful"})
	} else {
		// Se o username ou password estiverem vazios, retorna um erro 401 (Unauthorized)
		http.Error(w, "Unauthorized", http.StatusUnauthorized)
	}
}

func main() {
	// Registra a função loginHandler para lidar com requisições no endpoint /login
	http.HandleFunc("/login", loginHandler)

	// Configura o servidor HTTP com tempos de espera para leitura, escrita e inatividade
	server := &http.Server{
		Addr:         ":8080",           // O servidor será executado na porta 8080
		ReadTimeout:  10 * time.Second,  // Tempo máximo para leitura de dados da requisição
		WriteTimeout: 10 * time.Second,  // Tempo máximo para escrita de dados na resposta
		IdleTimeout:  120 * time.Second, // Tempo máximo de inatividade antes de fechar a conexão
	}

	// Exibe uma mensagem informando que o servidor está em execução
	println("Server is running on port 8080")

	// Inicia o servidor e, caso ocorra um erro, exibe uma mensagem de erro
	if err := server.ListenAndServe(); err != nil {
		println("Server error:", err)
	}
}
