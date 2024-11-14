import logging
import time
from flask import Flask, request, jsonify
import requests
import os
import psutil
from flask_cors import CORS
import random
import json
from flask_socketio import SocketIO, emit

LOG_FILE = 'app.log'

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})
    socketio = SocketIO(app, cors_allowed_origins="*")  # Suporte para WebSockets
    
    logging.basicConfig(
        filename=LOG_FILE, level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    BASE_URL = 'https://webto.salesforce.com/servlet/servlet.WebToLead?encoding=UTF-8'

    def update_resource_usage():
        cpu_usage = psutil.cpu_percent()
        memory_usage = psutil.virtual_memory().percent
        return cpu_usage, memory_usage

    def log_metrics(metrics):
        """Log metrics to the log file in JSON format."""
        logging.info(json.dumps(metrics))
        socketio.emit('metrics_update', metrics)  # Envia métricas para os clientes conectados em tempo real

    def update_average_response_time(current_avg, elapsed_time, total_requests):
        return ((current_avg * (total_requests - 1) + elapsed_time) / total_requests)

    def register_error(error_message, metrics):
        error_type = str(error_message)
        metrics["errors_by_type"][error_type] = metrics["errors_by_type"].get(error_type, 0) + 1

    def log_request_info():
        """Log user information including IP and User-Agent."""
        user_ip = mock_ip()  # Mocked IP address
        location = mock_location()  # Mocked location
        logging.info(f"Request from IP: {user_ip}, Location: {location}, Method: {request.method}")

    def mock_location():
        """Retorna uma localização fictícia (Cidade, Estado, País)."""
        locations = [
            ("New York", "NY", "USA"),
            ("São Paulo", "SP", "Brazil"),
            ("Tokyo", "Tokyo", "Japan"),
            ("Berlin", "Berlin", "Germany"),
        ]
        return random.choice(locations)

    def mock_ip():
        """Gera um IP fictício para as requisições."""
        return f"192.168.{random.randint(0, 255)}.{random.randint(0, 255)}"

    @app.route('/restHelper/processVoucher', methods=['POST'])
    def process_voucher():
        data = request.get_json()
        start_time = time.time()
        log_request_info()  # Log user info
        metrics = {
            "success_requests": 0,
            "failed_requests": 0,
            "average_response_time": 0,
            "total_requests": 0,
            "cpu_usage": 0,
            "memory_usage": 0,
            "errors_by_type": {},
            "user_ip": {},
            "location": {}
        }
        try:
            logging.info(f"Received data for processVoucher: {data}")
            cpu_usage, memory_usage = update_resource_usage()
            response = requests.post(f"{BASE_URL}/restHelper/processVoucher", json=data, headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {os.environ.get("TOKEN")}',
            })
            end_time = time.time()
            elapsed_time = end_time - start_time
            metrics["user_ip"] = mock_ip()
            metrics["location"] = mock_location()
            metrics["total_requests"] += 1
            metrics["average_response_time"] = update_average_response_time(
                metrics["average_response_time"], elapsed_time, metrics["total_requests"]
            )
            metrics["cpu_usage"] = cpu_usage
            metrics["memory_usage"] = memory_usage
            if response.status_code == 200:
                metrics["success_requests"] += 1
                logging.info(f"Voucher processed successfully in {elapsed_time:.2f} seconds")
            else:
                metrics["failed_requests"] += 1
                register_error(response.status_code, metrics)
                logging.error(f"Failed to process voucher: {response.status_code} - Took {elapsed_time:.2f} seconds")
            log_metrics(metrics)
            return jsonify({"status": "Voucher processed"} if response.status_code == 200 else {"error": "Failed to process voucher"}), response.status_code
        except requests.exceptions.RequestException as e:
            elapsed_time = time.time() - start_time
            metrics["failed_requests"] += 1
            register_error(e, metrics)
            logging.error(f"Error in processVoucher: {str(e)} - Took {elapsed_time:.2f} seconds")
            log_metrics(metrics)
            return jsonify({'error': str(e)}), 500

    @app.route('/restHelper/persistLoyalty', methods=['POST'])
    def persist_loyalty():
        data = request.get_json()
        start_time = time.time()
        log_request_info()  # Log user info
        metrics = {
            "success_requests": 0,
            "failed_requests": 0,
            "average_response_time": 0,
            "total_requests": 0,
            "cpu_usage": 0,
            "memory_usage": 0,
            "errors_by_type": {},
            "user_ip": {},
            "location": {}
        }
        try:
            logging.info(f"Received data for persistLoyalty: {data}")
            cpu_usage, memory_usage = update_resource_usage()
            response = requests.post(f"{BASE_URL}/restHelper/persistLoyalty", json=data, headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {os.environ.get("TOKEN")}',
            })
            end_time = time.time()
            elapsed_time = end_time - start_time
            metrics["user_ip"] = mock_ip()
            metrics["location"] = mock_location()
            metrics["total_requests"] += 1
            metrics["average_response_time"] = update_average_response_time(
                metrics["average_response_time"], elapsed_time, metrics["total_requests"]
            )
            metrics["cpu_usage"] = cpu_usage
            metrics["memory_usage"] = memory_usage
            if random.random() > 0.1 and response.status_code == 200:
                metrics["success_requests"] += 1
                logging.info(f"Loyalty persisted successfully in {elapsed_time:.2f} seconds")
            else:
                metrics["failed_requests"] += 1
                register_error(random.choice(["Timeout", "ConnectionError", "HTTPError"]), metrics)
                logging.error(f"Failed to persist loyalty: {response.status_code} - Took {elapsed_time:.2f} seconds")
            log_metrics(metrics)
            return jsonify({"status": "Loyalty persisted"} if response.status_code == 200 else {"error": "Failed to persist loyalty"}), response.status_code
        except requests.exceptions.RequestException as e:
            elapsed_time = time.time() - start_time
            metrics["failed_requests"] += 1
            register_error(e, metrics)
            logging.error(f"Error in persistLoyalty: {str(e)} - Took {elapsed_time:.2f} seconds")
            log_metrics(metrics)
            return jsonify({'error': str(e)}), 500

    @app.route('/health', methods=['GET'])
    def health_check():
        log_request_info()  # Log user info
        logging.info("Health check called")
        update_resource_usage()
        return jsonify({"status": "Service running"}), 200

    @socketio.on('connect')
    def handle_connect():
        print("Client connected")

    @app.route('/metrics', methods=['GET'])
    def get_metrics():
        log_request_info()  # Log user info
        logging.info("Metrics endpoint called")
        aggregated_metrics = {
            "success_requests": 0,
            "failed_requests": 0,
            "average_response_time": 0,
            "total_requests": 0,
            "cpu_usage": 0,
            "memory_usage": 0,
            "errors_by_type": {},
            "user_ip": {},
            "location": {}
        }
        try:
            with open(LOG_FILE, 'r') as log_file:
                for line in log_file:
                    if "INFO" in line:
                        try:
                            log_data = json.loads(line.split('INFO - ')[1])
                            aggregated_metrics["user_ip"] = mock_ip()
                            aggregated_metrics["location"] = mock_location()
                            aggregated_metrics["success_requests"] += log_data["success_requests"]
                            aggregated_metrics["failed_requests"] += log_data["failed_requests"]
                            aggregated_metrics["total_requests"] += log_data["total_requests"]
                            aggregated_metrics["average_response_time"] = update_average_response_time(
                                aggregated_metrics["average_response_time"],
                                log_data["average_response_time"],
                                aggregated_metrics["total_requests"]
                            )
                            aggregated_metrics["cpu_usage"] = log_data["cpu_usage"]
                            aggregated_metrics["memory_usage"] = log_data["memory_usage"]
                            for error_type, count in log_data["errors_by_type"].items():
                                aggregated_metrics["errors_by_type"][error_type] = aggregated_metrics["errors_by_type"].get(error_type, 0) + count
                        except json.JSONDecodeError:
                            continue
        except FileNotFoundError:
            return jsonify({"error": "Log file not found."}), 404
        return jsonify(aggregated_metrics), 200

    @socketio.on('request_metrics')
    def send_metrics():
        """Emite métricas a cada segundo para o frontend."""
        while True:
            cpu_usage, memory_usage = update_resource_usage()
            metrics = {
                "cpu_usage": cpu_usage,
                "memory_usage": memory_usage,
                "timestamp": time.time()  # Opcional: timestamp para marcar o tempo
            }
            log_metrics(metrics)
            socketio.emit('metrics_update', metrics)
            socketio.sleep(1)  # A cada segundo, envia as métricas

    return app, socketio

if __name__ == '__main__':
    app, socketio = create_app()
    socketio.run(app, debug=True)
