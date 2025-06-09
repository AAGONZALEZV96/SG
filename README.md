# SG Backend - Sistema de Gestión

Backend Flask con Serverless Framework y DynamoDB Local para desarrollo.

## 🚀 Configuración Inicial

### Prerrequisitos
- Python 3.12+
- Node.js 18+
- npm o yarn

### Instalación

1. **Clonar el repositorio**
\`\`\`bash
git clone <tu-repo>
cd sg-backend
\`\`\`

2. **Instalar dependencias**
\`\`\`bash
npm install
pip install -r requirements.txt
\`\`\`

3. **Configurar DynamoDB Local**
\`\`\`bash
npm run dynamodb:install
\`\`\`

## 🛠️ Desarrollo Local

### Opción 1: Comando único (Recomendado)
\`\`\`bash
npm run dev
\`\`\`
Esto ejecuta DynamoDB Local + Backend simultáneamente.

### Opción 2: Comandos separados
\`\`\`bash
# Terminal 1: DynamoDB Local
npm run dynamodb:start

# Terminal 2: Backend
npm run start
\`\`\`

### Poblar base de datos
\`\`\`bash
npm run seed
\`\`\`

## 🔗 Endpoints Disponibles

### Autenticación
- `POST /auth/login` - Iniciar sesión

### Usuarios
- `GET /users` - Listar usuarios
- `GET /users/{id}` - Obtener usuario
- `POST /users` - Crear usuario
- `PUT /users/{id}` - Actualizar usuario
- `DELETE /users/{id}` - Eliminar usuario

### Asistencia
- `GET /attendance` - Listar asistencias
- `POST /attendance` - Registrar asistencia

### Calificaciones
- `GET /grades` - Listar calificaciones
- `POST /grades` - Crear calificación

## 🗄️ Base de Datos

### Tablas
- `users-table-dev` - Usuarios del sistema
- `attendance-table-dev` - Registros de asistencia
- `grades-table-dev` - Calificaciones

### Datos de Prueba
Después de ejecutar `npm run seed`:

**👑 Admin:**
- Email: admin@sistema.com
- Password: admin123

**👩‍🏫 Teacher:**
- Email: teacher@sistema.com  
- Password: teacher123

**🎓 Student:**
- Email: student@sistema.com
- Password: student123

## 🐳 Docker (Opcional)

\`\`\`bash
# Ejecutar con Docker Compose
docker-compose up -d

# Ver logs
docker-compose logs -f

# Detener
docker-compose down
\`\`\`

## 📝 Scripts Disponibles

- `npm run dev` - Desarrollo completo
- `npm run start` - Solo backend
- `npm run dynamodb:start` - Solo DynamoDB
- `npm run dynamodb:install` - Instalar DynamoDB Local
- `npm run seed` - Poblar datos de prueba
- `npm run deploy` - Deploy a AWS

## 🔧 Configuración

### Variables de Entorno
Ver `.env.local` para configuración local.

### Serverless
Ver `serverless.yml` para configuración de deployment.

## 🚀 Deployment

\`\`\`bash
# Deploy a AWS
npm run deploy

# Deploy a stage específico
serverless deploy --stage production
