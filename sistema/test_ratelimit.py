# Arquivo: test_ratelimit.py
import requests
import time
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Desativa os avisos sobre certificados SSL não verificados (necessário para localhost)
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# --- CONFIGURAÇÕES DO TESTE ---
# URL completa da sua rota de login
LOGIN_URL = "https://localhost:3443/api/auth/login"

# Número de requisições a serem enviadas
NUM_REQUESTS = 30

# Payload de exemplo (não precisa ser válido, só para enviar no corpo da requisição)
DUMMY_PAYLOAD = {"username": "test_dos", "password": "password"}

# --- EXECUÇÃO DO TESTE ---
print(f"Iniciando teste de Rate Limiting na URL: {LOGIN_URL}")
print(f"Enviando {NUM_REQUESTS} requisições o mais rápido possível...")

success_count = 0
ratelimit_count = 0
error_count = 0

for i in range(NUM_REQUESTS):
    try:
        # verify=False é necessário para aceitar o certificado autoassinado do seu ambiente
        response = requests.post(LOGIN_URL, json=DUMMY_PAYLOAD, verify=False, timeout=5)
        
        # A resposta 401 (Credenciais Inválidas) significa que a requisição PASSOU pelo Nginx
        # e foi processada pela aplicação, o que é um sucesso para o nosso teste de rate limit.
        if response.status_code == 401:
            success_count += 1
            print(f"Requisição {i+1}/{NUM_REQUESTS}: Sucesso (Status {response.status_code}) - Passou pelo Nginx")
        # A resposta 503 significa que o Nginx BLOQUEOU a requisição
        elif response.status_code == 503:
            ratelimit_count += 1
            print(f"Requisição {i+1}/{NUM_REQUESTS}: BLOQUEADA (Status {response.status_code}) - Rate Limit Funcionou!")
        else:
            error_count += 1
            print(f"Requisição {i+1}/{NUM_REQUESTS}: Erro Inesperado (Status {response.status_code})")

    except requests.exceptions.RequestException as e:
        error_count += 1
        print(f"Requisição {i+1}/{NUM_REQUESTS}: Erro de Conexão - {e}")
    
    # Pequena pausa para não sobrecarregar a máquina local
    time.sleep(0.1)

print("\n--- RESULTADO DO TESTE ---")
print(f"Requisições Permitidas (Status 401): {success_count}")
print(f"Requisições Bloqueadas (Status 503): {ratelimit_count}")
print(f"Outros Erros: {error_count}")

if ratelimit_count > 0:
    print("\nSUCESSO!")
else:
    print("\nFALHA!")