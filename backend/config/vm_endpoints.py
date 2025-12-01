#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuración de endpoints de VMs para Capibara6
Este archivo contiene las URLs de conexión a los servicios en las diferentes VMs
"""

import os
import json
from typing import Dict, Optional

# Intentar cargar configuración desde archivo JSON si existe
VM_CONFIG_FILE = os.path.join(os.path.dirname(__file__), "../../vm_config.json")


def load_vm_config() -> Optional[Dict]:
    """Carga la configuración de VMs desde archivo JSON"""
    if os.path.exists(VM_CONFIG_FILE):
        try:
            with open(VM_CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"⚠️  Error cargando vm_config.json: {e}")
    return None


# Configuración por defecto - VMs actuales
# Red VPC: default (10.204.0.0/24) - Zona: europe-southwest1-b
# Actualizado: 2025-11-27
DEFAULT_VM_ENDPOINTS = {
    "models-europe": {
        "ip_external": os.getenv("MODELS_EUROPE_IP_EXTERNAL", "34.175.48.2"),
        "ip_internal": os.getenv("MODELS_EUROPE_IP_INTERNAL", "10.204.0.9"),
        "ollama": {
            "endpoint": os.getenv("OLLAMA_ENDPOINT", "http://10.204.0.9:11434"),
            "port": 11434,
            "models": ["gpt-oss:20b", "mistral:latest", "phi3:mini"]
        }
    },
    "rag-europe": {
        "ip_external": os.getenv("RAG_EUROPE_IP_EXTERNAL", "34.175.110.120"),
        "ip_internal": os.getenv("RAG_EUROPE_IP_INTERNAL", "10.204.0.10"),
        "bridge_api": {
            "endpoint": os.getenv("BRIDGE_API_ENDPOINT", "http://10.204.0.10:8000"),
            "port": 8000
        },
        "rag_api": {
            "endpoint": os.getenv("RAG_API_ENDPOINT", "http://10.204.0.10:8000"),
            "port": 8000
        },
        "nebula_studio": {
            "endpoint": os.getenv("NEBULA_STUDIO_ENDPOINT", "http://10.204.0.10:7001"),
            "port": 7001
        },
        "nebula_graph": {
            "endpoint": os.getenv("NEBULA_GRAPH_ENDPOINT", "http://10.204.0.10:9669"),
            "port": 9669
        },
        "milvus": {
            "endpoint": os.getenv("MILVUS_ENDPOINT", "http://10.204.0.10:19530"),
            "port": 19530
        }
    },
    "services": {
        "ip_external": os.getenv("SERVICES_IP_EXTERNAL", "34.175.255.139"),
        "ip_internal": os.getenv("SERVICES_IP_INTERNAL", "10.204.0.5"),
        "tts": {
            "endpoint": os.getenv("TTS_ENDPOINT", "http://10.204.0.5:5001"),
            "port": 5001
        },
        "mcp": {
            "endpoint": os.getenv("MCP_ENDPOINT", "http://10.204.0.5:5003"),
            "port": 5003
        },
        "n8n": {
            "endpoint": os.getenv("N8N_ENDPOINT", "http://10.204.0.5:5678"),
            "port": 5678
        },
        "flask_api": {
            "endpoint": os.getenv("FLASK_API_ENDPOINT", "http://10.204.0.5:5000"),
            "port": 5000
        },
        "nginx": {
            "endpoint": os.getenv("NGINX_ENDPOINT", "http://10.204.0.5:80"),
            "port": 80
        }
    }
}


class VMEndpoints:
    """Gestor de endpoints de VMs"""
    
    def __init__(self):
        self.config = load_vm_config() or {}
        self.endpoints = self._build_endpoints()
    
    def _build_endpoints(self) -> Dict:
        """Construye los endpoints usando configuración de archivo o valores por defecto"""
        endpoints = DEFAULT_VM_ENDPOINTS.copy()

        # Si hay configuración desde archivo, usarla
        if self.config.get("service_endpoints"):
            file_endpoints = self.config["service_endpoints"]

            # Actualizar endpoints de models-europe
            if "models-europe" in file_endpoints:
                endpoints["models-europe"].update(file_endpoints["models-europe"])

            # Actualizar endpoints de rag-europe
            if "rag-europe" in file_endpoints:
                endpoints["rag-europe"].update(file_endpoints["rag-europe"])

            # Actualizar endpoints de services
            if "services" in file_endpoints:
                endpoints["services"].update(file_endpoints["services"])

        return endpoints
    
    def get_ollama_endpoint(self, use_internal: bool = True) -> str:
        """Obtiene el endpoint de Ollama en models-europe"""
        vm_info = self.endpoints.get("models-europe", {})
        ollama = vm_info.get("ollama", {})

        if use_internal and vm_info.get("ip_internal"):
            return f"http://{vm_info['ip_internal']}:{ollama.get('port', 11434)}"
        elif vm_info.get("ip_external"):
            return f"http://{vm_info['ip_external']}:{ollama.get('port', 11434)}"

        return ollama.get("endpoint", "http://localhost:11434")

    def get_rag_endpoint(self, use_internal: bool = True) -> str:
        """Obtiene el endpoint del RAG API en rag-europe"""
        vm_info = self.endpoints.get("rag-europe", {})
        rag_api = vm_info.get("rag_api", {})

        if use_internal and vm_info.get("ip_internal"):
            return f"http://{vm_info['ip_internal']}:{rag_api.get('port', 8000)}"
        elif vm_info.get("ip_external"):
            return f"http://{vm_info['ip_external']}:{rag_api.get('port', 8000)}"

        return rag_api.get("endpoint", "http://localhost:8000")

    def get_bridge_endpoint(self, use_internal: bool = True) -> str:
        """Obtiene el endpoint del Bridge API en rag-europe"""
        vm_info = self.endpoints.get("rag-europe", {})
        bridge = vm_info.get("bridge_api", {})

        if use_internal and vm_info.get("ip_internal"):
            return f"http://{vm_info['ip_internal']}:{bridge.get('port', 8000)}"
        elif vm_info.get("ip_external"):
            return f"http://{vm_info['ip_external']}:{bridge.get('port', 8000)}"

        return bridge.get("endpoint", "http://localhost:8000")

    def get_tts_endpoint(self, use_internal: bool = True) -> str:
        """Obtiene el endpoint de TTS en services"""
        vm_info = self.endpoints.get("services", {})
        tts = vm_info.get("tts", {})

        if use_internal and vm_info.get("ip_internal"):
            return f"http://{vm_info['ip_internal']}:{tts.get('port', 5001)}"
        elif vm_info.get("ip_external"):
            return f"http://{vm_info['ip_external']}:{tts.get('port', 5001)}"

        return tts.get("endpoint", "http://localhost:5001")

    def get_mcp_endpoint(self, use_internal: bool = True) -> str:
        """Obtiene el endpoint de MCP en services"""
        vm_info = self.endpoints.get("services", {})
        mcp = vm_info.get("mcp", {})

        if use_internal and vm_info.get("ip_internal"):
            return f"http://{vm_info['ip_internal']}:{mcp.get('port', 5003)}"
        elif vm_info.get("ip_external"):
            return f"http://{vm_info['ip_external']}:{mcp.get('port', 5003)}"

        return mcp.get("endpoint", "http://localhost:5003")

    def get_n8n_endpoint(self, use_internal: bool = True) -> str:
        """Obtiene el endpoint de N8n en services"""
        vm_info = self.endpoints.get("services", {})
        n8n = vm_info.get("n8n", {})

        if use_internal and vm_info.get("ip_internal"):
            return f"http://{vm_info['ip_internal']}:{n8n.get('port', 5678)}"
        elif vm_info.get("ip_external"):
            return f"http://{vm_info['ip_external']}:{n8n.get('port', 5678)}"

        return n8n.get("endpoint", "http://localhost:5678")

    def get_flask_api_endpoint(self, use_internal: bool = True) -> str:
        """Obtiene el endpoint de Flask API en services"""
        vm_info = self.endpoints.get("services", {})
        flask = vm_info.get("flask_api", {})

        if use_internal and vm_info.get("ip_internal"):
            return f"http://{vm_info['ip_internal']}:{flask.get('port', 5000)}"
        elif vm_info.get("ip_external"):
            return f"http://{vm_info['ip_external']}:{flask.get('port', 5000)}"

        return flask.get("endpoint", "http://localhost:5000")
    
    def are_vms_in_same_vpc(self) -> bool:
        """Verifica si las VMs están en la misma VPC"""
        # Las VMs actuales están en la misma VPC por defecto
        # Red: default (10.204.0.0/24) - Zona: europe-southwest1-b
        if self.config.get("network", {}).get("same_vpc"):
            return True

        # Verificar manualmente
        networks = set()
        for vm_name in ["models-europe", "rag-europe", "services"]:
            vm_data = self.config.get("vms", {}).get(vm_name, {})
            if vm_data.get("network"):
                networks.add(vm_data["network"])

        # Si no hay configuración, asumir que están en la misma VPC
        return len(networks) <= 1

    def get_all_endpoints(self, use_internal: bool = True) -> Dict[str, str]:
        """Obtiene todos los endpoints en un diccionario"""
        return {
            "ollama": self.get_ollama_endpoint(use_internal),
            "rag_api": self.get_rag_endpoint(use_internal),
            "bridge_api": self.get_bridge_endpoint(use_internal),
            "tts": self.get_tts_endpoint(use_internal),
            "mcp": self.get_mcp_endpoint(use_internal),
            "n8n": self.get_n8n_endpoint(use_internal),
            "flask_api": self.get_flask_api_endpoint(use_internal)
        }


# Instancia global
vm_endpoints = VMEndpoints()


if __name__ == "__main__":
    print("🔗 Endpoints de VMs de Capibara6")
    print("=" * 60)
    print()
    
    print("📡 Endpoints (usando IPs internas si están disponibles):")
    endpoints = vm_endpoints.get_all_endpoints(use_internal=True)
    for service, endpoint in endpoints.items():
        print(f"  {service:12s}: {endpoint}")
    
    print()
    print("🌐 Estado de Red:")
    if vm_endpoints.are_vms_in_same_vpc():
        print("  ✅ Todas las VMs están en la misma VPC")
    else:
        print("  ⚠️  Las VMs NO están en la misma VPC")
    
    print()
    print("💡 Para actualizar la configuración:")
    print("   1. Ejecuta: python3 scripts/get_vm_info.py")
    print("   2. O configura variables de entorno:")
    print("      export OLLAMA_ENDPOINT=http://IP:11434")
    print("      export RAG_API_ENDPOINT=http://IP:8000")
    print("      etc.")

