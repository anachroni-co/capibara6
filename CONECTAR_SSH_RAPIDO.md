# 🚀 Solución Rápida para Conectar por SSH

## 🔴 Si se queda bloqueado en "Existing host keys found..."

### Opción 1: Presionar Enter
- Simplemente presiona **Enter**
- O escribe **yes** si te pregunta algo

### Opción 2: Cancelar y Reconectar (Ctrl + C)
```bash
# Cancelar con Ctrl + C
# Luego ejecutar con flag --quiet
gcloud compute ssh gemma-3-12b --zone=europe-southwest1-b --quiet
```

### Opción 3: SSH desde Google Cloud Console (MÁS FÁCIL)
1. Ir a: https://console.cloud.google.com/compute/instances?project=mamba-001
2. Buscar: `gemma-3-12b`
3. Click en botón **SSH** (al lado del nombre)
4. Se abre terminal en el navegador ✅

### Opción 4: Forzar Regeneración de Claves
```bash
# Eliminar claves antiguas
rm ~/.ssh/google_compute_known_hosts

# Reconectar
gcloud compute ssh gemma-3-12b --zone=europe-southwest1-b
```

## 🎯 RECOMENDACIÓN: Usar SSH desde el Navegador

Es más rápido y no tiene problemas de claves:
1. https://console.cloud.google.com/compute/instances?project=mamba-001
2. Click en **SSH** junto a `gemma-3-12b`
3. ¡Listo! Terminal abierta

## 🔧 Una vez conectado, ejecutar:

```bash
# Ver qué hay instalado
ls -la ~/
ps aux | grep -i llama
which ollama
```

---

**Si sigue bloqueado:** Usa el SSH del navegador (opción más fácil)
