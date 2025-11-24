# 🔀 Git Merge: Resolver Conflictos con --ours y --theirs

## 📋 Conceptos Básicos

Durante un merge en Git, cuando hay conflictos puedes elegir qué versión mantener:

### `--ours` (La nuestra)
- **Mantiene la versión de TU rama actual** (la rama donde estás haciendo el merge)
- Es la versión "local" / "actual"

### `--theirs` (La de ellos)
- **Mantiene la versión de la rama que estás mergeando** (la que viene de afuera)
- Es la versión "remota" / "externa" / "la que viene de fuera"

## 🎯 Ejemplo Práctico

Supongamos que estás en la rama `main` y haces merge de `origin/main`:

```bash
# Estás en: main (rama local)
git merge origin/main
# Conflictos...

# Si quieres la versión TUYA (la local):
git checkout --ours archivo.txt

# Si quieres la versión REMOTA (la que viene de afuera/origin):
git checkout --theirs archivo.txt
```

## 📝 Comandos para Resolver Conflictos

### 1. Ver qué archivos tienen conflictos

```bash
git status
# O más detallado:
git diff --name-only --diff-filter=U
```

### 2. Mantener tu versión (local/actual) - `--ours`

```bash
# Para un archivo específico
git checkout --ours archivo.txt

# Para todos los archivos con conflictos
git checkout --ours .
```

### 3. Mantener la versión remota (de afuera) - `--theirs`

```bash
# Para un archivo específico
git checkout --theirs archivo.txt

# Para todos los archivos con conflictos
git checkout --theirs .
```

## 🔍 Cuándo usar cada uno

### Usar `--ours` cuando:
- ✅ Quieres mantener **tu versión local** (la que tienes en tu rama)
- ✅ Tu versión tiene cambios que no quieres perder
- ✅ La versión remota tiene cambios incorrectos

### Usar `--theirs` cuando:
- ✅ Quieres mantener **la versión remota/externa** (la que viene de afuera)
- ✅ La versión remota tiene cambios más recientes o correctos
- ✅ Quieres sobrescribir tu versión local con la remota

## 💡 Ejemplo Completo: "Quiero el de afuera"

```bash
# 1. Hacer merge y detectar conflictos
git merge origin/main
# Auto-merging archivo.txt
# CONFLICT (content): Merge conflict in archivo.txt

# 2. Ver el estado
git status
# Unmerged paths:
#   both modified:   archivo.txt

# 3. Si quieres la versión DE AFUERA (remota/origin):
git checkout --theirs archivo.txt

# 4. Agregar el archivo resuelto
git add archivo.txt

# 5. Completar el merge
git commit
```

## 🎨 Para Todos los Archivos

Si quieres resolver TODOS los conflictos de la misma manera:

```bash
# Mantener TODA la versión remota (de afuera)
git checkout --theirs .

# O mantener TODA tu versión local
git checkout --ours .

# Luego agregar todo
git add .

# Completar el merge
git commit
```

## ⚠️ Importante: Diferencia en Rebase vs Merge

### En un Merge:
```bash
git merge origin/main
# --ours = tu rama actual (main)
# --theirs = la rama que merges (origin/main)
```

### En un Rebase:
```bash
git rebase origin/main
# --ours = origin/main (¡cuidado! se invierten)
# --theirs = tu rama (se invierten los roles)
```

**En rebase es al revés** porque rebase cambia de contexto:
- Durante rebase: `--ours` es la rama base y `--theirs` es tu rama

## 🔧 Comandos Adicionales Útiles

### Ver ambas versiones del conflicto

```bash
# Ver los cambios de tu versión (ours)
git diff --ours archivo.txt

# Ver los cambios de la versión remota (theirs)
git diff --theirs archivo.txt

# Ver ambos lados
git diff --ours --theirs archivo.txt
```

### Resolver conflicto manualmente con editor

```bash
# Abrir el archivo en tu editor favorito
code archivo.txt  # VS Code
vim archivo.txt   # Vim
nano archivo.txt  # Nano

# Buscar los marcadores:
# <<<<<<< HEAD (tu versión)
# =======
# >>>>>>> branch-name (versión remota)

# Editar manualmente y guardar
# Luego:
git add archivo.txt
git commit
```

### Abortar un merge si cambias de opinión

```bash
git merge --abort
```

## 📚 Resumen Rápido

| Situación | Comando | Resultado |
|-----------|---------|-----------|
| Quiero **MI versión** (local) | `git checkout --ours archivo.txt` | Mantiene tu código |
| Quiero **la versión REMOTA** (de afuera) | `git checkout --theirs archivo.txt` | Mantiene código remoto |
| Quiero resolver **todos** con versión remota | `git checkout --theirs .` | Todos los archivos |
| Quiero resolver **todos** con mi versión | `git checkout --ours .` | Todos los archivos |

## 🎯 Respuesta Directa a tu Pregunta

**"¿Cómo se hace para mantener el de afuera?"**

```bash
git checkout --theirs archivo.txt
```

O para todos los archivos:
```bash
git checkout --theirs .
```

Luego:
```bash
git add .
git commit
```

---

**¿Necesitas ayuda con un merge específico?** Comparte la situación y te ayudo a resolverlo.

