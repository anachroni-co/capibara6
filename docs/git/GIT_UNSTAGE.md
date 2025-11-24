# 📤 Git: Quitar Archivos del Staging (Unstage)

## 🎯 Respuesta Rápida

Para quitar un archivo del staging (área de preparación):

```bash
# Método moderno (recomendado, Git 2.23+)
git restore --staged archivo.txt

# Método clásico (funciona en todas las versiones)
git reset HEAD archivo.txt
```

## 📋 Comandos para Unstage

### 1. Quitar UN archivo del staging

```bash
# Método moderno (recomendado)
git restore --staged archivo.txt

# Método clásico (funciona siempre)
git reset HEAD archivo.txt
```

### 2. Quitar TODOS los archivos del staging

```bash
# Método moderno
git restore --staged .

# Método clásico
git reset HEAD
```

### 3. Quitar varios archivos específicos

```bash
git restore --staged archivo1.txt archivo2.txt archivo3.txt
```

### 4. Ver qué está en staging antes de quitar

```bash
# Ver estado actual
git status

# Ver qué está en staging
git diff --staged

# Ver lista de archivos en staging
git diff --staged --name-only
```

## 🔍 Diferencias entre los Comandos

### `git restore --staged` (Moderno, Git 2.23+)

```bash
git restore --staged archivo.txt
```

**Ventajas:**
- ✅ Más intuitivo y legible
- ✅ Específico para unstaging
- ✅ No modifica el archivo (solo lo quita del staging)

### `git reset HEAD` (Clásico)

```bash
git reset HEAD archivo.txt
```

**Ventajas:**
- ✅ Funciona en versiones antiguas de Git
- ✅ Ampliamente conocido

**Nota:** `git reset` puede hacer más cosas, pero con `HEAD` solo quita del staging.

## 📊 Ejemplo Completo

```bash
# 1. Agregar archivos al staging (por error)
git add archivo1.txt archivo2.txt archivo3.txt

# 2. Ver qué está en staging
git status
# Changes to be committed:
#   modified:   archivo1.txt
#   modified:   archivo2.txt
#   modified:   archivo3.txt

# 3. Quitar archivo1.txt del staging
git restore --staged archivo1.txt

# 4. Verificar el cambio
git status
# Changes to be committed:
#   modified:   archivo2.txt
#   modified:   archivo3.txt
# Changes not staged for commit:
#   modified:   archivo1.txt  ← Ahora está fuera del staging

# 5. Quitar todos los archivos restantes del staging
git restore --staged .

# 6. Verificar que todo está fuera del staging
git status
# Changes not staged for commit:
#   modified:   archivo1.txt
#   modified:   archivo2.txt
#   modified:   archivo3.txt
```

## ⚠️ Importante: ¿Se Pierden los Cambios?

**NO**, los cambios NO se pierden. Solo se quita del área de staging.

### Lo que pasa:

```
Antes de git add:
  Working Directory: ✅ archivo.txt (con cambios)
  Staging Area:      ❌ vacío

Después de git add:
  Working Directory: ✅ archivo.txt (con cambios)
  Staging Area:      ✅ archivo.txt (listo para commit)

Después de git restore --staged archivo.txt:
  Working Directory: ✅ archivo.txt (con cambios - SE MANTIENEN)
  Staging Area:      ❌ vacío
```

**Los cambios en el archivo se mantienen**, solo se quita del staging.

## 🎯 Casos de Uso Comunes

### 1. Agregaste un archivo por error

```bash
# Agregaste todos los archivos
git add .

# Te das cuenta que archivo.txt no debería estar incluido
git restore --staged archivo.txt
```

### 2. Quieres hacer commits separados

```bash
# Agregaste varios archivos
git add archivo1.txt archivo2.txt archivo3.txt

# Decides hacer commits separados
git restore --staged archivo2.txt archivo3.txt

# Commit solo archivo1.txt
git commit -m "Cambios en archivo1"

# Luego agregar y commitear los demás
git add archivo2.txt
git commit -m "Cambios en archivo2"
```

### 3. Cambiaste de opinión antes de commitear

```bash
# Ya agregaste archivos
git add archivo.txt

# Cambiaste de opinión, quieres revisarlos más
git restore --staged archivo.txt

# Ahora puedes editarlo y luego volver a agregarlo
git add archivo.txt
```

## 🔧 Comandos Relacionados Útiles

### Ver diferencias en staging

```bash
# Ver qué cambios están en staging
git diff --staged

# Ver diferencias específicas de un archivo en staging
git diff --staged archivo.txt
```

### Ver diferencias fuera de staging

```bash
# Ver cambios que NO están en staging
git diff

# Ver diferencias de un archivo específico
git diff archivo.txt
```

### Deshacer cambios en un archivo (no solo unstaging)

```bash
# ⚠️ CUIDADO: Esto SÍ pierde los cambios del archivo
# Restaurar el archivo a su estado en HEAD (último commit)
git restore archivo.txt

# O método clásico
git checkout -- archivo.txt
```

**Diferencia:**
- `git restore --staged archivo.txt` → Solo quita del staging (mantiene cambios)
- `git restore archivo.txt` → Restaura el archivo (PIERDE cambios)

## 📚 Resumen de Comandos

| Acción | Comando | Descripción |
|--------|---------|-------------|
| **Quitar UN archivo del staging** | `git restore --staged archivo.txt` | Solo quita del staging |
| **Quitar TODOS del staging** | `git restore --staged .` | Limpia el staging |
| **Quitar del staging (clásico)** | `git reset HEAD archivo.txt` | Método antiguo |
| **Ver qué está en staging** | `git status` o `git diff --staged` | Revisar estado |
| **Agregar al staging** | `git add archivo.txt` | Volver a agregar |

## 💡 Tips

1. **Usa `git status` frecuentemente** para ver qué está en staging
2. **`git restore --staged` no pierde cambios** - solo quita del staging
3. **Si quieres deshacer cambios completamente**, usa `git restore archivo.txt` (sin `--staged`)
4. **Puedes combinar con otros comandos**:
   ```bash
   git restore --staged archivo1.txt archivo2.txt
   ```

---

**¿Necesitas ayuda con algún caso específico?** Comparte tu situación y te ayudo.

