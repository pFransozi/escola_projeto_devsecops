FROM python:3.11-slim
WORKDIR /app

# Instala dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia código e certificados
COPY . .

# instala a ferramenta de certificados do Debian
RUN apt-get update \
 && apt-get install -y ca-certificates \
 && rm -rf /var/lib/apt/lists/*

COPY certs/mkcert-rootCA.pem /usr/local/share/ca-certificates/mkcert-rootCA.crt
RUN update-ca-certificates

RUN apt-get update \
 && apt-get install -y ca-certificates \
 && cp certs/mkcert-rootCA.pem /usr/local/share/ca-certificates/mkcert-rootCA.crt \
 && update-ca-certificates

# Exponha a porta 5002
EXPOSE 5002

# Comando padrão (pode usar ENTRYPOINT também)
CMD ["python", "app.py"]
