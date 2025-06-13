# Dockerfile para sistema/api-gateway/

# Etapa 1: Base e instalação de dependências
FROM python:3.11-slim
WORKDIR /app

# Copia e instala as dependências primeiro para aproveitar o cache do Docker
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# --- CORREÇÃO DEFINITIVA ---
# Em vez de um 'COPY . .', copiamos explicitamente o que é necessário.
# Isso garante que o app.py e a pasta certs sejam incluídos.
COPY app.py ./
COPY certs ./certs/

# Instala os certificados raiz no sistema operacional do contêiner
RUN apt-get update && apt-get install -y ca-certificates && rm -rf /var/lib/apt/lists/*
COPY certs/mkcert-rootCA.pem /usr/local/share/ca-certificates/mkcert-rootCA.crt
RUN update-ca-certificates

# Expõe a porta que a aplicação usa
EXPOSE 5002

# Comando para iniciar a aplicação
CMD ["python", "app.py"]
