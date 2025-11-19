# Arquitectura de Capibara6 - Sistema Multi-VM

## 🏗️ Visión General

Capibara6 utiliza una arquitectura distribuida con dos VMs de Google Cloud configuradas para proporcionar servicios especializados.

## 📦 Infraestructura

### VM 1: Modelos (Bounty) - 34.12.166.76
- **Puerto 8080**: GPT-OSS-20B (Modelo de lenguaje)
- **Puerto 5001**: Backend API Flask

### VM 2: Servicios - 34.175.136.104
- **Puerto 5002**: TTS (Text-to-Speech)
- **Puerto 5003**: MCP (Model Context Protocol)
- **Puerto 5678**: N8N (Automatización)

## 🚀 Inicio Rápido

Usa el script de inicio:
```bash
cd ~/capibara6
./START_CHAT.sh
```

Para más detalles, consulta `backend/README.md`
