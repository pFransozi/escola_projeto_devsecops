# Etapa 1: Build do React
FROM node:20-alpine AS builder

WORKDIR /app

COPY package*.json ./
COPY .env .env
RUN npm install

COPY . .
RUN npm run build

# Etapa 2: Servir com Nginx
FROM nginx:alpine

# Copia a build gerada
COPY --from=builder /app/build /usr/share/nginx/html

# Copia o arquivo de configuração do Nginx (opcional)
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
