# Instrucciones para Diagnóstico de VM rag3

## ⚠️ Problema Detectado

No puedo acceder directamente a la VM rag3 desde este entorno porque:
- Google Cloud SDK (gcloud) no está instalado en este entorno
- No hay configuración SSH disponible

## 🔧 Solución: Script de Diagnóstico Automatizado

He creado un script completo (`vm_rag3_diagnostic.sh`) que recopilará toda la información necesaria sobre:
- ✅ Milvus Database
- ✅ Nebula Graph
- ✅ ChromaDB
- ✅ Servidor Bridge
- ✅ Todos los servicios RAG
- ✅ Configuraciones y puertos activos

---

## 📋 Pasos para Ejecutar el Diagnóstico

### Opción 1: Ejecutar el Script Directamente (Recomendado)

```bash
# 1. Copiar el script a la VM rag3
gcloud compute scp --zone "europe-west2-c" vm_rag3_diagnostic.sh rag3:~/ --project "mamba-001"

# 2. Conectarse a la VM
gcloud compute ssh --zone "europe-west2-c" "rag3" --project "mamba-001"

# 3. Hacer el script ejecutable y ejecutarlo
chmod +x vm_rag3_diagnostic.sh
./vm_rag3_diagnostic.sh

# 4. El script creará un archivo de reporte con timestamp
# Ejemplo: vm_rag3_diagnostic_20251113_212345.txt

# 5. Ver el contenido del reporte
cat vm_rag3_diagnostic_*.txt

# 6. Copiar el nombre completo del archivo y descargarlo
# (ejecutar desde tu máquina local, NO desde la VM)
exit  # Salir de la VM primero
gcloud compute scp --zone "europe-west2-c" rag3:~/vm_rag3_diagnostic_*.txt . --project "mamba-001"
```

Luego, comparte el contenido del archivo conmigo.

---

### Opción 2: Ejecutar Comandos Manualmente

Si prefieres ejecutar los comandos manualmente, conéctate a la VM y ejecuta:

```bash
gcloud compute ssh --zone "europe-west2-c" "rag3" --project "mamba-001"
```

Una vez conectado, ejecuta estos comandos y comparte los resultados:

#### 1. Información Básica del Sistema
```bash
echo "=== SISTEMA ==="
hostname
uname -a
cat /etc/os-release
```

#### 2. Puertos en Escucha
```bash
echo "=== PUERTOS ==="
sudo netstat -tlnp | grep -E "19530|9559|9779|9669|8000|7687"
# O si netstat no está disponible:
sudo ss -tlnp | grep -E "19530|9559|9779|9669|8000|7687"
```

#### 3. Procesos en Ejecución
```bash
echo "=== PROCESOS ==="
ps aux | grep -E "milvus|nebula|chroma|bridge|rag" | grep -v grep
```

#### 4. Contenedores Docker
```bash
echo "=== DOCKER ==="
sudo docker ps
sudo docker ps -a
sudo docker images
```

#### 5. Servicios Systemd
```bash
echo "=== SERVICIOS ==="
systemctl list-units --type=service --state=running | grep -E "milvus|nebula|chroma"
```

#### 6. Instalaciones de Software
```bash
echo "=== SOFTWARE INSTALADO ==="

# Milvus
which milvus || echo "Milvus no en PATH"
find /opt /usr/local -name "*milvus*" -type d 2>/dev/null

# Nebula Graph
which nebula-graphd || echo "Nebula no en PATH"
find /opt /usr/local -name "*nebula*" -type d 2>/dev/null

# ChromaDB
pip3 list | grep -i chroma || echo "ChromaDB no en pip"
```

#### 7. Archivos del Proyecto
```bash
echo "=== PROYECTOS ==="
find /home -maxdepth 3 -type d -name "*capibara*" -o -name "*rag*" -o -name "*bridge*" 2>/dev/null

# Listar archivos Python relevantes
find /home -maxdepth 4 -name "*.py" | grep -E "bridge|rag|milvus|nebula|chroma"
```

#### 8. Paquetes Python
```bash
echo "=== PYTHON PACKAGES ==="
python3 --version
pip3 list | grep -E "milvus|pymilvus|nebula|chroma|chromadb|langchain|faiss"
```

#### 9. Probar Endpoints
```bash
echo "=== ENDPOINTS ==="
curl -s http://localhost:19530 || echo "Puerto 19530 no accesible (Milvus)"
curl -s http://localhost:9669 || echo "Puerto 9669 no accesible (Nebula)"
curl -s http://localhost:8000 || echo "Puerto 8000 no accesible (ChromaDB/Bridge)"
```

---

## 🎯 Lo Que Estoy Buscando

### 1. **Milvus Database**
- **Puerto esperado:** 19530
- **Servicio:** Vector database para RAG
- **Comando para verificar:**
  ```bash
  sudo netstat -tlnp | grep 19530
  ps aux | grep milvus
  ```

### 2. **Nebula Graph**
- **Puertos esperados:**
  - 9559 (Meta service)
  - 9779 (Storage service)
  - 9669 (Query service)
- **Servicio:** Graph database
- **Comando para verificar:**
  ```bash
  sudo netstat -tlnp | grep -E "9559|9779|9669"
  ps aux | grep nebula
  ```

### 3. **ChromaDB**
- **Puerto esperado:** 8000 (por defecto)
- **Servicio:** Vector database alternativo
- **Comando para verificar:**
  ```bash
  pip3 list | grep chroma
  ps aux | grep chroma
  ```

### 4. **Servidor Bridge**
- **Puerto esperado:** Desconocido (probablemente 8000, 5000, o 5001)
- **Servicio:** Bridge entre frontend y backends
- **Comando para verificar:**
  ```bash
  find /home -name "*bridge*.py"
  ps aux | grep bridge
  ```

---

## 📊 Puertos Esperados - Resumen

| Puerto | Servicio | Descripción |
|--------|----------|-------------|
| 19530 | Milvus | Vector database |
| 9559 | Nebula Meta | Graph DB metadata |
| 9779 | Nebula Storage | Graph DB storage |
| 9669 | Nebula Query | Graph DB queries |
| 8000 | ChromaDB/Bridge | Vector DB o API bridge |
| 7687 | Neo4j (alt) | Si se usa Neo4j en lugar de Nebula |

---

## 📤 Cómo Compartir los Resultados Conmigo

### Si usaste el script de diagnóstico:
```bash
# Desde tu máquina local (NO desde la VM)
gcloud compute scp --zone "europe-west2-c" rag3:~/vm_rag3_diagnostic_*.txt . --project "mamba-001"

# Luego copia y pega el contenido del archivo en nuestra conversación
cat vm_rag3_diagnostic_*.txt
```

### Si ejecutaste comandos manualmente:
Simplemente copia y pega la salida de los comandos en nuestra conversación.

---

## 🚀 Próximos Pasos

Una vez que tenga la información de la VM rag3, podré:

1. ✅ Documentar todos los servicios encontrados
2. ✅ Actualizar `INFRASTRUCTURE_FINDINGS.md` con los hallazgos
3. ✅ Crear configuración de conexión para estos servicios
4. ✅ Actualizar scripts de gestión para incluir verificación de servicios remotos
5. ✅ Documentar la arquitectura completa del sistema RAG
6. ✅ Crear scripts de integración si es necesario

---

## ⚠️ Nota Importante

Si la VM rag3 no tiene algunos de estos servicios instalados, necesitaremos:
- Instalarlos, O
- Actualizar la documentación para reflejar la arquitectura real, O
- Implementar alternativas usando FAISS (que ya está configurado)

El script de diagnóstico nos dirá exactamente qué está instalado y qué no, para que podamos planear los siguientes pasos de manera precisa.
