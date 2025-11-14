# 🔧 Solución para Scripts Bloqueados

## ❌ Problema

Los scripts de gcloud se quedan "congelados" o no muestran salida.

## 🔍 Diagnóstico

Los comandos `gcloud compute ssh` pueden tardar mucho tiempo porque:
1. Establecen conexión SSH (puede tardar 10-30 segundos)
2. Esperan autenticación SSH
3. Ejecutan comandos remotos
4. La salida puede no mostrarse inmediatamente

## ✅ Soluciones

### Opción 1: Ejecutar Comandos Manualmente Uno por Uno

En lugar de ejecutar scripts, ejecuta comandos individuales:

```bash
# Verificar bounty2
gcloud compute ssh bounty2 --zone=europe-west4-a --project=mamba-001 --command="ps aux | grep python | head -5"

# Verificar rag3
gcloud compute ssh rag3 --zone=europe-west2-c --project=mamba-001 --command="ps aux | grep python | head -5"

# Verificar gpt-oss-20b
gcloud compute ssh gpt-oss-20b --zone=europe-southwest1-b --project=mamba-001 --command="ps aux | grep python | head -5"
```

### Opción 2: Usar Scripts con Timeout

He creado scripts con timeouts más cortos:

```bash
# Script con timeouts cortos
./verificar_con_timeout.sh

# Script directo con filtrado de salida
./verificar_servicios_directo.sh
```

### Opción 3: Conectarse Interactivamente

Conéctate directamente a cada VM y ejecuta comandos localmente:

```bash
# Conectarse a bounty2
gcloud compute ssh bounty2 --zone=europe-west4-a --project=mamba-001

# Una vez dentro, ejecutar:
ps aux | grep python
sudo ss -tuln | grep -E ':(5001|11434)'
curl http://localhost:5001/api/health
```

### Opción 4: Usar Comandos Más Simples

En lugar de scripts complejos, usa comandos simples:

```bash
# Solo verificar si la VM responde
gcloud compute ssh bounty2 --zone=europe-west4-a --project=mamba-001 --command="hostname"

# Ver procesos
gcloud compute ssh bounty2 --zone=europe-west4-a --project=mamba-001 --command="ps aux | grep python | wc -l"
```

## 🐛 Si los Comandos Siguen Bloqueados

### Verificar Procesos Bloqueados

```bash
# Ver procesos gcloud corriendo
ps aux | grep gcloud | grep -v grep

# Matar procesos bloqueados
pkill -f "gcloud.*ssh"
```

### Verificar Autenticación

```bash
# Ver cuentas autenticadas
gcloud auth list

# Ver proyecto actual
gcloud config get-value project

# Verificar permisos
gcloud projects get-iam-policy mamba-001
```

### Usar Modo Verbose

```bash
# Ver qué está pasando
gcloud compute ssh bounty2 --zone=europe-west4-a --project=mamba-001 --command="hostname" --verbosity=debug
```

## 💡 Recomendación

**Ejecuta comandos manualmente uno por uno** en lugar de scripts automáticos:

1. **Primero verifica acceso básico**:
```bash
gcloud compute instances list --project=mamba-001
```

2. **Luego conecta a cada VM individualmente**:
```bash
gcloud compute ssh bounty2 --zone=europe-west4-a --project=mamba-001
```

3. **Una vez dentro, ejecuta comandos localmente**:
```bash
ps aux | grep python
sudo ss -tuln | grep 5001
curl http://localhost:5001/api/health
```

## 📝 Comandos Rápidos para Verificar

### bounty2
```bash
gcloud compute ssh bounty2 --zone=europe-west4-a --project=mamba-001 --command="ps aux | grep -E '(python|ollama)' | grep -v grep"
```

### rag3
```bash
gcloud compute ssh rag3 --zone=europe-west2-c --project=mamba-001 --command="ps aux | grep python | grep -v grep"
```

### gpt-oss-20b
```bash
gcloud compute ssh gpt-oss-20b --zone=europe-southwest1-b --project=mamba-001 --command="ps aux | grep python | grep -v grep"
```

---

**Última actualización**: Noviembre 2025

