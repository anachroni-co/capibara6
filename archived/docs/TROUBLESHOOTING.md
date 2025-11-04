# 🔧 Solución de Problemas - Capibara6

## ✅ Estado Actual del Sistema

- **Consenso:** DESHABILITADO (por ahora)
- **Modelo activo:** Capibara6 (Gemma3-12B)
- **Servidor:** http://34.175.89.158:8080

## 🔍 Verificar Conectividad

### 1. Verificar que el servidor de Capibara6 esté respondiendo:

```bash
curl -X POST http://34.175.89.158:8080/completion -H "Content-Type: application/json" -d "{\"prompt\":\"Hola\",\"n_predict\":10}"
```

### 2. Iniciar solo el frontend:

```cmd
cd web
python -m http.server 8000
```

### 3. Abrir el navegador:

```
http://localhost:8000/chat.html
```

## 🚨 Problemas Comunes

### Problema: "El servidor no responde"

**Causas posibles:**
- El servidor de Capibara6 no está corriendo
- Problemas de red/firewall
- CORS bloqueando la petición

**Solución:**
1. Verificar que el servidor esté online
2. Comprobar la consola del navegador (F12)
3. Verificar configuración CORS

### Problema: "Authentication required"

**Solución:**
- Si no quieres usar autenticación, comenta la verificación en `chat-app.js`:

```javascript
// Comentar estas líneas en la función init():
// if (!checkAuthentication()) {
//     return;
// }
```

### Problema: "Consensus server unreachable"

**Solución:**
- Esto es normal, el consenso está deshabilitado por ahora
- El error se puede ignorar

## 🔄 Para Habilitar el Consenso Más Tarde

1. Editar `web/chat-app.js`:
   ```javascript
   const CONSENSUS_CONFIG = {
       enabled: true,  // Cambiar a true
       // ...
   };
   ```

2. Descomentar en `web/chat.html`:
   ```html
   <script src="consensus-integration.js"></script>
   ```

3. Iniciar servidor de consenso:
   ```cmd
   python backend/consensus_server.py
   ```

4. Configurar URL del OSS-120B en `backend/models_config.py`

## 📋 Comandos Útiles

### Ver logs del navegador:
```
F12 > Console
```

### Limpiar caché del navegador:
```
Ctrl + Shift + Delete
```

### Limpiar localStorage:
```javascript
// En consola del navegador:
localStorage.clear();
location.reload();
```

## 🆘 Si Nada Funciona

1. **Limpiar todo y empezar de cero:**
   ```cmd
   # Borrar caché del navegador
   # Cerrar todas las ventanas del navegador
   # Reiniciar el servidor
   cd web
   python -m http.server 8000
   ```

2. **Verificar configuración:**
   - ✅ `MODEL_CONFIG.serverUrl` apunta a `http://34.175.89.158:8080/completion`
   - ✅ `consensusEnabled = false`
   - ✅ Script `consensus-integration.js` comentado
   - ✅ No hay errores en consola del navegador

3. **Contactar soporte:**
   - Compartir logs de la consola del navegador
   - Compartir respuesta del curl al servidor
   - Describir el comportamiento exacto

## ✅ Checklist de Verificación

- [ ] Servidor frontend corriendo en puerto 8000
- [ ] Navegador puede acceder a http://localhost:8000
- [ ] Consola del navegador sin errores críticos
- [ ] Configuración de `MODEL_CONFIG` correcta
- [ ] `consensusEnabled = false`
- [ ] Script de consenso comentado

---

**Estado:** Sistema simplificado usando solo Capibara6 original
**Última actualización:** 2025-01-08
