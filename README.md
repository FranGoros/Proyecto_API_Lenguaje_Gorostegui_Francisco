# Proyecto de facultad para la materia de Lenguaje

API REST de gestion de videojuegos, usuarios, favoritos y recomendaciones.

# Tecnologías
- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic

# Funcionalidades
- CRUD de videojuegos
- CRUD de usuarios
- Filtros de videojuegos
- Sistema de favoritos
- Sistema de recomendaciones
- Base de datos SQLite
- Documentación automática con Swagger

# Cómo ejecutar el proyecto?

# 1 Crear y activar el entorno virtual
python -m venv venv
.\venv\Scripts\Activate.ps1

# 2 Instalar las dependencias
pip install fastapi uvicorn sqlalchemy

# 3 Ejecutar la API
uvicorn main:app --reload

# 4 Abrir la documentación