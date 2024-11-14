from flask import Flask, request, jsonify
import time
import random
from datetime import datetime

app = Flask(__name__)

# Simulação de uma base de dados de usuários
users_db = {
    "cogny_user": {"password": "securepassword"},
    "another_user": {"password": "anotherpassword"}
}

# Registro de tentativas de login suspeitas
suspicious_users = {}

# Lista de IPs bloqueados
blocked_ips = set()

def simulate_delay():
    """Simula um delay de processamento no servidor entre 10 ms e 50 ms."""
    time.sleep(random.uniform(0.01, 0.05))

def log_suspicious_attempt(username, ip_address):
    """Registra tentativas de login suspeitas."""
    if username not in suspicious_users:
        suspicious_users[username] = {
            "attempts": [],
            "blocked_ips": set()
        }
    suspicious_users[username]["attempts"].append({
        "timestamp": datetime.now().isoformat(),
        "ip_address": ip_address
    })

def detect_suspicious_activity():
    """Detecta atividades suspeitas com base nas tentativas de login."""
    time_window = 60  # 1 minuto
    failure_threshold = 5  # Número de falhas permitido na janela

    for username, data in suspicious_users.items():
        recent_attempts = [
            attempt for attempt in data["attempts"]
            if (datetime.now() - datetime.fromisoformat(attempt["timestamp"])).total_seconds() <= time_window
        ]
        if len(recent_attempts) >= failure_threshold:
            for attempt in recent_attempts:
                data["blocked_ips"].add(attempt["ip_address"])
            print(f"Usuário suspeito detectado e IPs bloqueados: {username} -> {data['blocked_ips']}")

def block_ip(ip_address):
    """Bloqueia um IP suspeito."""
    blocked_ips.add(ip_address)
    print(f"IP bloqueado: {ip_address}")

# Rota de login da Cogny
@app.route('/cogny/login', methods=['POST'])
def cogny_login():
    simulate_delay()
    data = request.json
    username = data.get('username')
    password = data.get('password')
    ip_address = request.remote_addr

    if ip_address in blocked_ips:
        return jsonify({"message": "Este IP está temporariamente bloqueado."}), 403

    if username in users_db and users_db[username]["password"] == password:
        return jsonify({"message": "Login bem-sucedido!", "user": username}), 200
    else:
        log_suspicious_attempt(username, ip_address)
        detect_suspicious_activity()
        return jsonify({"message": "Usuário ou senha incorretos."}), 401

# Rota para exibir usuários suspeitos e suas tentativas de login
@app.route('/cogny/suspicious_users', methods=['GET'])
def get_suspicious_users():
    """Retorna os usuários suspeitos e suas tentativas de login."""
    serialized_users = {
        username: {
            "attempts": data["attempts"],
            "blocked_ips": list(data["blocked_ips"])
        }
        for username, data in suspicious_users.items()
    }
    return jsonify(serialized_users), 200

# Rota para rodar a prevenção e mostrar o status
@app.route('/cogny/run_prevention', methods=['GET'])
def run_prevention():
    """Executa a predição e prevenção e retorna o status."""
    detect_suspicious_activity()
    
    if suspicious_users:
        serialized_users = {
            username: {
                "attempts": data["attempts"],
                "blocked_ips": list(data["blocked_ips"])
            }
            for username, data in suspicious_users.items()
        }
        return jsonify({"message": "Detectamos algo suspeito!", "details": serialized_users}), 200
    return jsonify({"message": "Todas as tentativas estão corretas."}), 200

if __name__ == '__main__':
    app.run(debug=True)
