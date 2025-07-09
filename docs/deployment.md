# Guía de Despliegue - Chatbot Panadería Jos y Mar

## 🚀 Despliegue en Railway

### Prerrequisitos
- Cuenta en Railway (railway.app)
- Código del proyecto subido a GitHub
- Variables de entorno configuradas

### Pasos de Despliegue

1. **Conectar GitHub a Railway**
   - Iniciar sesión en Railway
   - Crear nuevo proyecto
   - Conectar repositorio de GitHub

2. **Configurar Base de Datos MySQL**
   ```
   - En Railway: Add Service → MySQL
   - Guardar credenciales de conexión
   ```

3. **Configurar Variables de Entorno**
   ```
   DB_HOST=containers-us-west-xxx.railway.app
   DB_PORT=7306
   DB_USER=root
   DB_PASSWORD=[password-generado]
   DB_NAME=railway
   FLASK_ENV=production
   PORT=5000
   ```

4. **Ejecutar Scripts de Base de Datos**
   - Conectarse a MySQL de Railway
   - Ejecutar `database/schema.sql`
   - Ejecutar `database/sample_data.sql`

5. **Desplegar Aplicación**
   - Railway detectará automáticamente la aplicación Flask
   - Usará `requirements.txt` para instalar dependencias
   - La aplicación se ejecutará con `gunicorn`

### Verificación Post-Despliegue

1. **Health Check**
   ```
   GET https://tu-app.railway.app/
   ```

2. **Test Base de Datos**
   ```
   GET https://tu-app.railway.app/test-db
   ```

3. **Test Productos**
   ```
   GET https://tu-app.railway.app/productos/pan_salado
   ```

### Configuración de Dominio (Opcional)
- En Railway → Settings → Custom Domain
- Configurar dominio personalizado si es necesario

## 📝 Comandos Útiles

### Para desarrollo local:
```bash
# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales

# Ejecutar aplicación
python app.py
```

### Para debugging:
```bash
# Ver logs en Railway
railway logs

# Conectar a base de datos Railway
railway connect mysql
```

## ⚠️ Notas Importantes

- El health check debe responder en `/`
- Railway asigna puerto automáticamente (variable PORT)
- La aplicación debe estar lista para producción
- Las credenciales de BD se generan automáticamente en Railway

## 🔧 Troubleshooting

### Error de Conexión a BD
```
- Verificar variables de entorno
- Confirmar que MySQL está ejecutándose en Railway
- Revisar credenciales de conexión
```

### Error en Despliegue
```
- Verificar requirements.txt
- Revisar logs de Railway
- Confirmar estructura de archivos
```

### Webhook no Responde
```
- Verificar URL del webhook
- Confirmar que la aplicación está ejecutándose
- Revisar logs de la aplicación
```
