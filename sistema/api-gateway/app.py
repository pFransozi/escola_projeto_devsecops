import os
import time
import logging
import json
from flask import Flask, request, Response
import requests
from dotenv import load_dotenv

# Carrega variáveis de .env
load_dotenv()

AUTH_SERVICE_URL    = os.getenv('AUTH_SERVICE_URL')
BACKEND_SERVICE_URL = os.getenv('BACKEND_SERVICE_URL')
if not AUTH_SERVICE_URL or not BACKEND_SERVICE_URL:
    raise RuntimeError("Defina AUTH_SERVICE_URL e BACKEND_SERVICE_URL no ambiente")

# Diretório e arquivo de log
LOG_DIR  = os.getenv('LOG_DIR', 'logs')
LOG_FILE = os.path.join(LOG_DIR, 'api_gateway.log')

# Garante que a pasta de logs exista
os.makedirs(LOG_DIR, exist_ok=True)

app = Flask(__name__)

# Formatter JSON simples
formatter = logging.Formatter('%(message)s')

# 1) Handler para stdout
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

# 2) Handler para arquivo
file_handler = logging.FileHandler(LOG_FILE)
file_handler.setFormatter(formatter)

# Configura logger do Flask
app.logger.handlers = [stream_handler, file_handler]
app.logger.setLevel(logging.INFO)

@app.before_request
def start_timer():
    """Inicia um temporizador no objeto request para medir a duração da requisição atual."""

    request.start_time = time.time()

@app.after_request
def log_request(response):
    """
    Registra detalhes da requisição após a resposta ser gerada.
    Calcula a duração da requisição, identifica o serviço de destino (auth ou backend),
    e loga informações como método HTTP, caminho, status e tempo de processamento em ms.
    """
    duration = time.time() - request.start_time
    client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    dest = 'auth' if request.path.startswith('/api/auth/') else 'backend'
    log_data = {
        'timestamp': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
        'ip': client_ip,
        'method': request.method,
        'path': request.path,
        'destination': dest,
        'status': response.status_code,
        'duration_ms': round(duration * 1000, 2)
    }
    # grava em stdout e no arquivo
    app.logger.info(json.dumps(log_data))
    return response

@app.route('/api/<path:subpath>', methods=['GET','POST','PUT','PATCH','DELETE'])
def gateway(subpath):
    """
    Rota principal do API Gateway.
    Redireciona a requisição recebida para o serviço apropriado (auth-service ou backend) com base no caminho.
    Encaminha método, headers, parâmetros de query, corpo e cookies para o serviço de destino.
    Retorna:
        A resposta HTTP recebida do serviço de destino, incluindo corpo, status e cabeçalhos relevantes.
    """
    # Escolhe o serviço alvo
    if subpath.startswith('auth/'):
        url = f"{AUTH_SERVICE_URL}/api/{subpath}"
    else:
        url = f"{BACKEND_SERVICE_URL}/api/{subpath}"

    # Repassa headers e corpo
    headers = {
        k: v for k, v in request.headers.items()
        if k.lower() not in ('host','content-length','connection')
    }

    resp = requests.request(
        method=request.method,
        url=url,
        headers=headers,
        params=request.args,
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False,
        verify=False
    )

    excluded = {'content-encoding','content-length','transfer-encoding','connection'}
    response_headers = [
        (k, v) for k, v in resp.headers.items()
        if k.lower() not in excluded
    ]
    return Response(resp.content, resp.status_code, response_headers)

if __name__ == '__main__':
    cert = os.getenv('SSL_CERT_PATH', 'certs/server.crt')
    key  = os.getenv('SSL_KEY_PATH' , 'certs/server.key')
    app.run(host='0.0.0.0', port=5002, ssl_context=(cert, key))
