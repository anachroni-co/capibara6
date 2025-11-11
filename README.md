# 🦫 Capibara6 - Chat de IA con GPT-OSS-20B

## ✅ Sistema Funcionando

**Backend**: http://34.12.166.76:5001
**Modelo**: gpt-oss:20b (20.9B parámetros via Ollama)
**Estado**: ✅ Operativo

## 🚀 Uso Rápido

### Iniciar Frontend
```bash
cd web
python3 -m http.server 8000
# Abre: http://localhost:8000/chat.html
```

### Test Backend
```bash
curl http://34.12.166.76:5001/api/health
```

## 📚 Documentación

- `QUICK_START.md` - Inicio rápido
- `OLLAMA_SETUP.md` - Configuración de Ollama  
- `VM_SETUP.md` - Gestión de VMs
- `backend/README.md` - Backend docs

## 🔧 Gestión

### Conectar a VMs
```bash
./ssh-bounty2.sh  # Modelos
./ssh-services.sh # Servicios
```

### Reiniciar Backend (en bounty2)
```bash
cd ~/capibara6/backend
pkill -f server_gptoss.py
python3 server_gptoss.py
```

---
**Anachroni s.coop** | marco@anachroni.co
