# Manual de Instrucciones para Proyecto E-commerce con Docker

## Descripción del Proyecto
Tienda en línea de electrodomésticos desarrollada con Django y SQLite, dockerizada para facilitar su ejecución.

## Requisitos Previos
### Instalación de Docker
1. Descargar Docker Desktop
2. Verificar instalación:
```bash
docker --version
docker-compose --version
```

## Estructura del Proyecto
### Archivos Principales
- `Dockerfile`: Definición de imagen Docker
- `docker-compose.yml`: Configuración de servicios
- `requirements.txt`: Dependencias del proyecto

### Directorios
- `/shop`: Catálogo de productos
- `/cart`: Carrito de compras
- `/orders`: Gestión de pedidos
- `/accounts`: Registro de usuarios

## Pasos de Ejecución

### 1. Construir Imagen de Docker
```bash
docker-compose build
```

### 2. Iniciar Contenedores
```bash
docker-compose up
```

### 3. Aplicar Migraciones
```bash
docker-compose exec web python manage.py migrate
```

### 4. Poblar Base de Datos
```bash
docker-compose exec web python populate_shop.py
```

### 5. Crear Superusuario
```bash
docker-compose exec web python manage.py createsuperuser
```

## Acceso a la Aplicación
- **Sitio web**: `http://localhost:8000`
- **Panel admin**: `http://localhost:8000/admin`

## Características
- Carrito de compras visible
- Métodos de pago: Contrareembolso y Stripe
- Opciones de envío
- Seguimiento de pedidos
- Gestión administrativa completa

## Detener Contenedores
```bash
docker-compose down
```

## Solución de Problemas
### Errores Comunes
1. **Puerto Ocupado**: Modificar en `docker-compose.yml`
   ```yaml
   ports: - "8001:8000"
   ```

2. **Migraciones**: Verificar ejecución del contenedor

3. **Datos Iniciales**: Ejecutar `populate_shop.py`
