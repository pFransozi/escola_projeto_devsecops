# # Etapa 1 - Build
# FROM node:18-alpine as builder
# WORKDIR /app
# COPY . .
# RUN npm install
# RUN npm run build

# # Etapa 2 - Servir via Nginx
# FROM nginx:alpine
# COPY --from=builder /app/dist /usr/share/nginx/html
# COPY nginx.conf /etc/nginx/conf.d/default.conf
# COPY cert.pem  /app/cert.pem
# COPY key.pem   /app/key.pem


# EXPOSE 80 
# EXPOSE 443
# CMD ["nginx", "-g", "daemon off;"]

# 1) Build stage: gera o dist com Vite
FROM node:18-alpine AS builder
WORKDIR /app

# 1.1) Instala dependências
COPY package*.json ./
RUN npm install

# 1.2) Copia todo o código e gera o build
COPY . .
RUN npm run build

# 2) Production stage: serve pelo Nginx
FROM nginx:stable-alpine

# 2.1) Copia certificados mkcert se for HTTPS no Nginx
# (se não quiser, basta omitir estas linhas)
COPY cert.pem  /etc/nginx/certs/cert.pem
COPY key.pem   /etc/nginx/certs/key.pem

# 2.2) Sobrescreve a config padrão do Nginx
#     (coloque seu nginx.conf ao lado do Dockerfile)
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 2.3) Copia os assets estáticos gerados pelo Vite
COPY --from=builder /app/dist /usr/share/nginx/html

# 2.4) Expõe HTTP e HTTPS
EXPOSE 80
EXPOSE 443

# 2.5) Inicia o Nginx
CMD ["nginx", "-g", "daemon off;"]

