#!/bin/bash

# Aplicar migraciones
python manage.py migrate

# Verificar si la base de datos está vacía y poblarla
if [ ! -f "db.sqlite3" ]; then
    echo "Poblando la base de datos..."
    python populate_shop.py
fi

# Iniciar el servidor
exec "$@"
