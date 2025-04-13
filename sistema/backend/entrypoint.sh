#!/bin/bash
set -e

echo "Iniciando o container do Flask Backend."

MYSQL_HOST=${MYSQL_HOST:-mysql_db}
echo "Aguardando o banco de dados MySQL em $MYSQL_HOST:3306..."

until nc -z "$MYSQL_HOST" 3306; do
  echo "Banco ainda não está disponível... tentando novamente em 1s."
  sleep 1
done

echo "Banco de dados está pronto."

# Verifica se o diretório de migração já existe
if [ ! -f "migrations/env.py" ]; then
  echo "Inicializando estrutura de migração (flask db init)..."
  flask db init
  echo "Criando primeira migração (flask db migrate)..."
  flask db migrate -m "Migração inicial automática"
fi

echo "Aplicando migrações (flask db upgrade)..."
flask db upgrade

echo "Verificando/criando usuário admin..."
python create_admin.py

echo "Iniciando servidor Flask..."
exec flask run --host=0.0.0.0 --port=5000
