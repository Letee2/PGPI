#!/bin/bash

# Salir inmediatamente si un comando falla
set -e

# Aplicar migraciones
echo "Aplicando migraciones..."
python manage.py migrate

# Poblar la base de datos
echo "Poblando la base de datos inicial..."
python populate_shop.py

# Crear un superusuario predefinido
echo "Creando superusuario..."
python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(email="admin@admin.com").exists():
    User.objects.create_superuser(email="admin@admin.com", password="admin")
    print("Superusuario admin@admin.com creado.")
else:
    print("Superusuario admin@admin.com ya existe.")
EOF

# Recolectar archivos estáticos
echo "Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

# Iniciar el servidor
echo "Iniciando el servidor..."
exec "$@"
