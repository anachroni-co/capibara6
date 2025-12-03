#!/usr/bin/env python3
"""
E2B Coordinador para VM Services
Este módulo permite a la VM services coordinar ejecuciones E2B en la VM models-europe
y retornar los resultados al frontend que también está en services.
"""

import requests
import json
import os
from typing import Dict, Any, Optional
from flask import Flask, request, jsonify, send_file
import tempfile
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class E2BCoordinator:
    def __init__(self, config_path: str = "/home/elect/capibara6/vm_coordination_config.json"):
        """
        Inicializa el coordinador E2B para comunicación entre VMs
        """
        with open(config_path, 'r') as f:
            self.config = json.load(f)

        # La ejecución E2B ocurre en models-europe (más rápida) pero el frontend está en la misma VM services
        self.models_europe_url = f"http://{self.config['vm_config']['models_europe']['internal_ip']}:{self.config['vm_config']['models_europe']['ports']['backend_api']}"
        self.execution_vm = self.config['e2b_coordination']['execution_vm']

        logger.info(f"E2B Coordinador inicializado - Ejecución E2B en: {self.execution_vm}")
        logger.info(f"URL destino para ejecución E2B: {self.models_europe_url}")
        logger.info(f"El frontend está en esta misma VM (services), los resultados se retornan directamente")

    def execute_e2b_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Ejecuta una tarea E2B en la VM models-europe y retorna los resultados al frontend
        """
        try:
            # Enviar la tarea a la VM models-europe para ejecución E2B (más rápida)
            e2b_endpoint = f"{self.models_europe_url}/api/e2b/process"
            logger.info(f"Enviando tarea E2B a: {e2b_endpoint} para ejecución más rápida")

            response = requests.post(
                e2b_endpoint,
                json=task_data,
                timeout=self.config['e2b_coordination']['timeout']
            )

            if response.status_code == 200:
                result = response.json()
                logger.info("Tarea E2B ejecutada exitosamente en models-europe")
                return {
                    "success": True,
                    "result": result,
                    "execution_vm": self.execution_vm,  # Indica donde se ejecutó
                    "message": f"E2B ejecutado en {self.execution_vm} y resultado retornado al frontend en services"
                }
            else:
                logger.error(f"Error en ejecución E2B: {response.status_code} - {response.text}")
                return {
                    "success": False,
                    "error": f"Error en la VM {self.execution_vm}: {response.status_code}",
                    "details": response.text
                }

        except requests.exceptions.RequestException as e:
            logger.error(f"Error de conexión con {self.execution_vm}: {e}")
            return {
                "success": False,
                "error": f"Error de conexión con la VM {self.execution_vm}",
                "details": str(e)
            }
        except Exception as e:
            logger.error(f"Error inesperado en coordinación E2B: {e}")
            return {
                "success": False,
                "error": "Error interno en coordinación E2B",
                "details": str(e)
            }

    def get_visualization_file(self, filepath: str) -> Optional[str]:
        """
        Obtiene un archivo de visualización desde la VM models-europe donde se generó
        """
        try:
            visualization_url = f"{self.models_europe_url}/api/e2b/visualization/{filepath}"
            logger.info(f"Solicitando archivo de visualización desde models-europe: {visualization_url}")

            response = requests.get(visualization_url, timeout=30)

            if response.status_code == 200:
                # Guardar archivo temporalmente para servirlo al frontend que está en esta VM (services)
                with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(filepath)[1]) as tmp_file:
                    tmp_file.write(response.content)
                    logger.info(f"Archivo de visualización descargado y listo para servir al frontend: {tmp_file.name}")
                    return tmp_file.name
            else:
                logger.error(f"Error al obtener visualización desde models-europe: {response.status_code}")
                return None

        except Exception as e:
            logger.error(f"Error al obtener archivo de visualización desde models-europe: {e}")
            return None

# Inicializar el coordinador
e2b_coordinator = E2BCoordinator()

# Crear la aplicación Flask para la VM services (donde está el frontend)
app = Flask(__name__)

@app.route('/api/e2b/execute', methods=['POST'])
def proxy_e2b_execution():
    """
    Endpoint para el frontend en services - coordina ejecución E2B en models-europe
    La ejecución ocurre en models-europe por velocidad, pero el resultado va al frontend en services
    """
    try:
        task_data = request.json
        logger.info("Recibida solicitud de ejecución E2B desde frontend local en services")

        # Ejecutar la tarea en models-europe (donde es más rápido) y retornar resultado al frontend
        result = e2b_coordinator.execute_e2b_task(task_data)

        return jsonify(result)

    except Exception as e:
        logger.error(f"Error en proxy de E2B: {e}")
        return jsonify({
            "success": False,
            "error": "Error interno en el proxy E2B",
            "details": str(e)
        }), 500

@app.route('/api/e2b/visualization/<path:filepath>', methods=['GET'])
def proxy_visualization_file(filepath):
    """
    Endpoint para servir archivos de visualización generados en models-europe al frontend en services
    """
    try:
        logger.info(f"Solicitud de archivo de visualización: {filepath}")

        # Obtener el archivo desde models-europe donde se generó
        temp_file_path = e2b_coordinator.get_visualization_file(filepath)

        if temp_file_path:
            logger.info(f"Sirviendo archivo de visualización al frontend local: {temp_file_path}")
            # Servir el archivo al frontend local en esta VM (services)
            return send_file(temp_file_path)
        else:
            logger.error(f"No se pudo obtener el archivo de visualización: {filepath}")
            return jsonify({"error": "Archivo de visualización no encontrado"}), 404

    except Exception as e:
        logger.error(f"Error al servir archivo de visualización al frontend: {e}")
        return jsonify({"error": "Error interno al servir archivo de visualización"}), 500

@app.route('/api/e2b/health', methods=['GET'])
def e2b_coordinator_health():
    """
    Endpoint para verificar el estado del coordinador E2B
    """
    try:
        # Probar conexión con models-europe donde se ejecuta E2B
        health_url = f"{e2b_coordinator.models_europe_url}/health"
        response = requests.get(health_url, timeout=10)

        models_health = response.status_code == 200
        models_data = response.json() if models_health else {}

        return jsonify({
            "status": "healthy",
            "coordinator": "active",
            "frontend_location": "services VM",  # El frontend está en esta VM
            "execution_location": "models-europe VM",  # La ejecución está en models-europe
            "models_europe_connection": models_health,
            "models_europe_e2b_available": models_data.get("e2b_available", False) if models_data else False,
            "execution_vm": e2b_coordinator.execution_vm
        })

    except Exception as e:
        logger.error(f"Error en health check de E2B: {e}")
        return jsonify({
            "status": "unhealthy",
            "execution_location": "models-europe VM",
            "frontend_location": "services VM",
            "error": str(e)
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5003))  # Usando puerto 5003 para coordinación E2B
    logger.info(f"Iniciando E2B Coordinador en puerto {port}, coordinando ejecución desde models-europe al frontend en services")
    app.run(host='0.0.0.0', port=port, debug=False)