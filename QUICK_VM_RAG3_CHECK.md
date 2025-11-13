# 🚀 Comando Rápido para Verificar VM rag3

## Copiar y Ejecutar (Todo en Uno)

Ejecuta estos comandos desde tu terminal local:

```bash
# 1. Copiar el script de diagnóstico a la VM
gcloud compute scp --zone "europe-west2-c" vm_rag3_diagnostic.sh rag3:~/ --project "mamba-001"

# 2. Ejecutar el script remotamente y ver el resultado inmediatamente
gcloud compute ssh --zone "europe-west2-c" "rag3" --project "mamba-001" --command "chmod +x ~/vm_rag3_diagnostic.sh && ~/vm_rag3_diagnostic.sh && cat ~/vm_rag3_diagnostic_*.txt"
```

El segundo comando se conectará, ejecutará el diagnóstico completo y mostrará los resultados automáticamente.

---

## O Versión Paso a Paso

```bash
# Copiar script
gcloud compute scp --zone "europe-west2-c" vm_rag3_diagnostic.sh rag3:~/ --project "mamba-001"

# Conectar y ejecutar
gcloud compute ssh --zone "europe-west2-c" "rag3" --project "mamba-001"

# Una vez dentro de la VM:
chmod +x vm_rag3_diagnostic.sh
./vm_rag3_diagnostic.sh
cat vm_rag3_diagnostic_*.txt
```

---

## Verificación Rápida Manual (Sin Script)

Si solo quieres una verificación rápida de 30 segundos:

```bash
gcloud compute ssh --zone "europe-west2-c" "rag3" --project "mamba-001" --command "
echo '=== PUERTOS EN ESCUCHA (Milvus 19530, Nebula 9669/9559/9779) ==='
sudo ss -tlnp | grep -E '19530|9669|9559|9779|8000' || echo 'Ninguno de los puertos esperados está en escucha'
echo ''
echo '=== PROCESOS ACTIVOS ==='
ps aux | grep -E 'milvus|nebula|chroma|bridge' | grep -v grep || echo 'No hay procesos relacionados'
echo ''
echo '=== DOCKER CONTAINERS ==='
sudo docker ps 2>/dev/null || echo 'Docker no está corriendo o no hay contenedores activos'
echo ''
echo '=== PYTHON PACKAGES ==='
pip3 list | grep -E 'milvus|nebula|chroma' || echo 'No hay paquetes Python relacionados instalados'
"
```

Esto te dará una respuesta rápida sobre si los servicios están corriendo.

---

## Qué Buscar en los Resultados

### ✅ Milvus Está Instalado Si Ves:
```
tcp        0      0 0.0.0.0:19530           0.0.0.0:*               LISTEN      12345/milvus
```

### ✅ Nebula Graph Está Instalado Si Ves:
```
tcp        0      0 0.0.0.0:9669            0.0.0.0:*               LISTEN      12346/nebula-graphd
tcp        0      0 0.0.0.0:9559            0.0.0.0:*               LISTEN      12347/nebula-metad
```

### ✅ ChromaDB Está Instalado Si Ves:
```
chromadb                  0.4.22
```

### ✅ Bridge Server Si Ves:
```
python3 /home/user/bridge_server.py
```

---

**Una vez tengas los resultados, compártelos conmigo y podré documentar toda la infraestructura de VM rag3.**
