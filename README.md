# Auth API - FastAPI

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue)
![JWT](https://img.shields.io/badge/Auth-JWT-orange)

API de autenticación construida con **FastAPI**, usando **PostgreSQL**, **JWT** y SQLAlchemy.

El proyecto implementa autenticación basada en tokens JWT con Access Token, Refresh Token, rutas protegidas, control de acceso por roles (RBAC) y blacklist de tokens para logout.

---

## Características

* Registro de usuarios
* Login con JWT Bearer Token
* Access Token + Refresh Token
* Refresh endpoint (`/auth/refresh`)
* Logout con revocación de tokens
* Hash seguro de contraseñas (**bcrypt**)
* Rutas protegidas con autenticación
* Control de acceso por roles (**admin / user**)
* Obtención del usuario actual desde el token
* Logout con revocación de **access token** usando blacklist en DB
* Arquitectura modular por capas
* Configuración mediante variables de entorno (`.env`)
* Identificación de usuarios mediante UUID

---

## Arquitectura

El proyecto está organizado usando separación de responsabilidades:

* Routes → Endpoints HTTP
* Services → Lógica de negocio
* Repositories → Acceso a datos
* Schemas → Validación y serialización
* Models → Modelos ORM SQLAlchemy
* Core → Seguridad, configuración y dependencias

---
## Modelo de Usuario

Los usuarios son identificados mediante UUID como clave primaria.

Ejemplo:

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@email.com",
  "role": "user"
}

##  Tecnologías

* Python 3.10+
* FastAPI
* SQLAlchemy
* PostgreSQL
* JWT (python-jose)
* Passlib (bcrypt)
* email-validator (para `EmailStr` en Pydantic)
* python-dotenv

---

## Estructura del proyecto

```text
app/
│
├── api/
│   └── v1/
│       └── routes/
│           ├── auth.py
│           └── user.py
│
├── core/
│   ├── config.py
│   ├── security.py
│   └── dependencies.py
│
├── db/
│   └── session.py
│
├── models/
│   ├── user.py
│   └── token_blacklist.py
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

```bash
git clone https://github.com/TU_USER/auth-api-fastapi.git
cd auth-api-fastapi
```

---

### 2. Crear entorno virtual

```bash
python -m venv venv
```

Activar:

```bash
# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

---

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

### 4. Configurar variables de entorno

Crear archivo `.env`:

```env
DATABASE_URL=postgresql://user:password@localhost/db_name
SECRET_KEY=supersecret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

---

## Archivo `.env.example`

```env
DATABASE_URL=
SECRET_KEY=
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

---

## ▶ Ejecutar servidor

```bash
uvicorn app.main:app --reload
```

Abrir en navegador:

 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## Autenticación

La API utiliza **JWT con esquema Bearer Token**.

### Header requerido

```http
Authorization: Bearer <your_token>
```

---

##  Flujo JWT

```text
Login
   ↓
Access Token + Refresh Token
   ↓
Access Token → rutas protegidas
   ↓
Token expira
   ↓
Refresh Token → /auth/refresh
   ↓
Nuevo Access Token
```

---

## Logout (Blacklist)

La API implementa una blacklist básica de tokens:

* Al hacer logout → el token se guarda en DB
* Tokens en blacklist → no pueden acceder

### Endpoint

```http
POST /auth/logout
Authorization: Bearer <access_token>
```

### Notas

* El logout actual **revoca únicamente el access token**.
* La validación de blacklist se aplica en rutas protegidas (por ejemplo `GET /users/me`).

---

##  Endpoints

###  Auth

#### Registro

```http
POST /auth/register
```

---

#### Login

```http
POST /auth/login
```

### Body

```json
{
  "email": "user@email.com",
  "password": "12345678"
}
```

### Respuesta

```json
{
  "access_token": "<access_token>",
  "refresh_token": "<refresh_token>",
  "token_type": "bearer"
}
```

---

#### Refresh Token

```http
POST /auth/refresh
```

### Body

```json
{
  "refresh_token": "<your_refresh_token>"
}
```

### Respuesta

```json
{
  "access_token": "<new_access_token>"
}
```

---

#### Logout

```http
POST /auth/logout
Authorization: Bearer <access_token>
```

---

### Usuarios

#### Obtener usuario actual

```http
GET /users/me
```

  Requiere autenticación.

### Respuesta

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@email.com",
  "role": "user"
}
```

---

###   Admin

#### Endpoint solo admin

```http
GET /users/admin
```

  Requiere rol `admin`

---

## 📡 Ejemplo Login con curl

```bash
curl -X POST "http://127.0.0.1:8000/auth/login" \
-H "Content-Type: application/json" \
-d '{
  "email": "admin@email.com",
  "password": "12345678"
}'
```

---

##   Status Codes

| Code | Description      |
| ---- | ---------------- |
| 200  | Success          |
| 201  | Resource created |
| 401  | Unauthorized     |
| 403  | Forbidden        |
| 409  | Conflict         |

---

##   Seguridad

* Contraseñas encriptadas con bcrypt
* Access Token y Refresh Token JWT
* Tokens JWT firmados
* Expiración configurable
* Validación de tipo de token
* Blacklist de tokens revocados
* Control de acceso por roles (RBAC)
* Variables sensibles protegidas en `.env`
* UTC timezone-aware datetimes
* UUID como identificador

---

##  Testing

Puedes probar la API con:

* Swagger UI (`/docs`)
* Postman

---

##  Notas (dependencias)

Si usas `EmailStr` en los schemas, asegúrate de tener instalado `email-validator`.

Si tu entorno no lo tiene, verás un error como:

```text
ImportError: email-validator is not installed
```

---

##  Flujo de trabajo (Git)

* `main` → producción
* `feature/*` → nuevas funcionalidades
* `fix/*` → corrección de errores
* `refactor/*` → refactorización
* `docs/*` → documentación

### Ejemplos

```bash
feature/jwt-auth
feature/token-blacklist
fix/token-validation
refactor/auth-service-layer
docs/readme-update
```

---

##  Conventional Commits

```bash
feat: implement JWT authentication flow
fix: validate refresh token correctly
refactor: separate auth logic into service layer
docs: improve README documentation
```

---


