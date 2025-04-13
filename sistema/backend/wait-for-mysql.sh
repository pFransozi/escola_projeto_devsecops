#!/bin/sh

echo "Aguardando o MySQL ficar disponível em $DB_HOST..."

while ! nc -z $DB_HOST 3306; do
  sleep 1
done

echo "MySQL está pronto! Iniciando Flask..."

exec "$@"
