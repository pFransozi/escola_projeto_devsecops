#!/bin/sh

# Exporta a variável de ambiente para o Flask encontrar a aplicação
export FLASK_APP=app

echo "Waiting for database..."
# Loop para esperar o container do banco de dados (db) ficar disponível na porta 3306
timeout=60
count=0
while ! nc -z db 3306; do
  sleep 1
  count=$((count+1))
  if [ $count -ge $timeout ]; then
    echo "Banco de dados não respondeu após $timeout segundos, abortando."
    exit 1
  fi
done
echo "Database connection is ready."

# Verifica se a pasta de migrações não existe
if [ ! -d "migrations" ]; then
    echo "Inicializando estrutura de migração (flask db init)..."
    # Cria a estrutura de migrações
    flask db init
    echo "Criando primeira migração (flask db migrate)..."
    # Cria o arquivo da migração inicial
    flask db migrate -m "Migração inicial automática"
fi

echo "Applying database migrations..."
# Aplica as migrações pendentes ao banco de dados
flask db upgrade

# Garante que todas as tabelas sejam criadas, como um fallback
echo "Ensuring all tables are created (db.create_all)..."
python - <<'EOF'
from app import create_app, db
app = create_app()
with app.app_context():
    db.create_all()
EOF

echo "Starting Flask development server..."
# Inicia a aplicação Flask, permitindo acesso de qualquer IP na porta 5000
#exec flask run --host=0.0.0.0 --port=5000

echo "Iniciando servidor Flask..."
# exec flask run --host=0.0.0.0 --port=5000
exec python -m app.main
