# Auth API - FastAPI

API de autenticación profesional construida con **FastAPI**, usando **PostgreSQL**, **JWT** y arquitectura por capas.

---

## 📌 Características

* Registro de usuarios
* Login con autenticación JWT
* Hash seguro de contraseñas (bcrypt)
* Arquitectura limpia (models, schemas, services, repositories)
* Configuración por variables de entorno (.env)
* Estructura escalable 

---

## Tecnologías

* Python 3.10+
* FastAPI
* SQLAlchemy
* PostgreSQL
* JWT (python-jose)
* Passlib (bcrypt)
* python-dotenv

---

## 📁 Estructura del proyecto

```
app/
│
├── api/
│   └── v1/
│       └── routes/
│           └── auth.py
│
├── core/
│   ├── config.py
│   └── security.py
│
├── db/
│   └── session.py
│
├── models/
│   └── user.py
│
├── schemas/
│   └── user.py
│
├── repositories/
│   └── user_repository.py
│
├── services/
│   └── auth_service.py
│
└── main.py
```

---

## Configuración del entorno

### 1. Clonar repositorio

```
git clone https://github.com/TU_USER/auth-api-fastapi.git
cd auth-api-fastapi
```

---

### 2. Crear entorno virtual

```
python -m venv venv
```

Activar:

```
# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

---

### 3. Instalar dependencias

```
pip install -r requirements.txt
```

---

### 4. Configurar variables de entorno

Crear archivo `.env`:

```
DATABASE_URL=postgresql://user:password@localhost/db_name
SECRET_KEY=supersecret
ALGORITHM=HS256
```

---

## ▶️ Ejecutar servidor

```
uvicorn app.main:app --reload
```

Abrir en navegador:

👉 http://127.0.0.1:8000/docs

---

## Endpoints

### 📌 Registro

```
POST /auth/register
```

### 📌 Login

```
POST /auth/login
```

Respuesta:

```
{
  "access_token": "JWT_TOKEN",
  "token_type": "bearer"
}
```

---

## 🧪 Testing manual

Puedes usar:

* Swagger UI (`/docs`)
* Postman


---

## Flujo de trabajo (Git)

* `main` → producción
* `feature/*` → nuevas funcionalidades
* `refactor/*` → mejoras de código

Ejemplo:

```
feature/auth
feature/env-config
refactor/add-comments
```

---

## Seguridad

* Contraseñas encriptadas con bcrypt
* Uso de variables de entorno (.env)
* Tokens JWT

---

## 🚀 Próximas mejoras

* Refresh tokens
* Protección de rutas
* Roles (admin/user)
* Docker
* Deploy (Render / Railway)
* Migraciones con Alembic

---

