# ⚙️ FDPEN Backend

Backend oficial de la **Federación Deportiva Provincial Estudiantil de Napo** - Plataforma para la **gestión de eventos deportivos estudiantiles**.

---

## 🛠 Tecnologías

### Core
- **🐍 Python 3.11+** - Lenguaje principal  
- **⚡ FastAPI** - Framework ASGI
- **🧱 SQLAlchemy Core** - Toolkit SQL y ORM (Core)  
- **📜 Alembic** - Migraciones de base de datos  
- **🧩 Pydantic** - Validación y serialización de datos  

### Base de Datos
- **🐘 PostgreSQL** - Base de datos relacional  

### Seguridad y Autenticación
- **🔐 python-jose** - Implementación de JWT  
- **🔒 bcrypt** - Hash de contraseñas  

### Desarrollo y Calidad
- **🚀 Uvicorn** - Servidor ASGI  
- **🔧 Ruff** - Linter y formatter
- **🐳 Docker** - Contenerización  

## 📁 Estructura del Proyecto

```
src/
├── core/                     # Núcleo compartido
│   ├── config.py             # Configuración (variables de entorno)
│   ├── database/             # Configuración de base de datos
│   │   ├── base.py           # Base para modelos SQLAlchemy
│   │   ├── engine.py         # Configuración del motor
│   │   ├── di.py             # Inyección de dependencias (DB, UoW)
│   │   └── uow_session.py    # Implementación de Unit of Work
│   ├── responses/            # Respuestas estandarizadas y excepciones
│   │   ├── helpers.py
│   │   └── exceptions.py
│   ├── security/             # Autenticación y autorización
│   │   ├── jwt_service.py    # Servicio JWT
│   │   ├── permissions.py    # Sistema de permisos
│   │   └── middleware.py     # Middleware de autenticación
│   └── email/                # Servicio de envío de email
│       ├── smtp_service.py
│       └── templates/
├── modules/                  # Módulos por dominio
│   ├── auth/
│   │   ├── api/              # Capa API (Endpoints FastAPI)
│   │   ├── application/      # Capa Aplicación (Casos de uso/Servicios)
│   │   ├── domain/           # Capa Dominio (Entidades y Reglas)
│   │   └── infrastructure/   # Capa Infraestructura (Repositorios, Modelos DB)
├── main.py                   # Punto de entrada de la aplicación FastAPI
└── models.py                 # Registro de modelos para Alembic
```

### 🧱 Organización y prácticas aplicadas


- **🎯 Principios SOLID:** Aplicación de Responsabilidad Única (SRP) e Inversión de Dependencias (DI).  
- **🧩 Repository Pattern:** Abstracción del acceso a datos.  
- **🔄 Unit of Work (UoW):** Gestión de transacciones atómicas en los casos de uso.  
- **📦 DTO Pattern:** Objetos de transferencia de datos.

## 🚀 Configuración Local

### Prerrequisitos

- **Python** >= 3.11  
- **PostgreSQL** >= 13  
- **Docker** (recomendado para la base de datos)  

---

### nstalación

## 🧱 Organización y prácticas aplicadas

- **🏗️ Clean Architecture:** Organización por capas (API, Application, Domain, Infrastructure).  
- **🎯 Principios SOLID:** Aplicación de Responsabilidad Única (SRP) e Inversión de Dependencias (DI).  
- **🧩 Repository Pattern:** Abstracción del acceso a datos.  
- **🔄 Unit of Work (UoW):** Gestión de transacciones atómicas en los casos de uso.  
- **📦 DTO Pattern (Pydantic):** Objetos de transferencia de datos para validación estricta.  

---

## 🚀 Configuración Local

### 🧩 Prerrequisitos

- **Python** >= 3.11  
- **PostgreSQL** >= 13  
- **Docker** (recomendado para la base de datos)  

---

### 🧰 Instalación y Configuración

1. **Clonar el repositorio**
```bash
git clone <repository-url>
cd <Proyecto>
```
2. **Configurar entorno virtual**
```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Windows:
.\venv\Scripts\activate
# En macOS/Linux:
source venv/bin/activate
```
3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```
4. **Configurar variables de entorno**
```bash
# Configuración del servidor
SECRET_KEY=clave_secreta
ALGORITHM=HS256

# Configuración de base de datos
POSTGRES_USER=user
POSTGRES_DB=name_db
DATABASE_PORT=port
POSTGRES_PASSWORD=password

# Configuración de email
SMTP_HOST=smtp.gmail.com
SMTP_PORT=port
SMTP_USER=email@gmail.com
SMTP_PASSWORD=password
SMTP_USE_TLS=true
DEFAULT_FROM_EMAIL=noreply@fdpen.edu.ec

# Configuración de URLs
FRONTEND_BASE_URL=http://localhost:5173
```

5. **Levantar Base de Datos (con Docker)**
```bash
docker-compose up -d
```

6. **Ejecutar Migraciones**
```bash
alembic upgrade head
```

7. **Ejecutar la Aplicación**
```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

8. **Verificar Instalación**
- **API:** [http://localhost:8000](http://localhost:8000)
- **Documentación (Swagger):** [http://localhost:8000/docs](http://localhost:8000/docs)
- **Documentación (Redoc):** [http://localhost:8000/redoc](http://localhost:8000/redoc)

## ⚙️ Configuración de VSCode

### Extensiones Recomendadas
```json
{
  "recommendations": [
    "astral.sh.ruff",
    "ms-python.python"
  ]
}
```

### Configuración (.vscode/settings.json)
```json
{
    "editor.defaultFormatter": "charliermarsh.ruff",
    "editor.formatOnSave": true,
    "ruff.lint.ignore": [
        "F401"
    ],
    "editor.codeActionsOnSave": {
        "source.organizeImports": "explicit",
        "source.fixAll": "explicit"
    }
}

```
