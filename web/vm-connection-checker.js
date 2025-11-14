/*
 * Script de comprobación de conexión a VM bounty2
 * 
 * Este script permite verificar que los servicios necesarios estén corriendo
 * y accesibles en la VM bounty2 antes de intentar conectarse desde el frontend.
 */

class VMConnectionChecker {
    constructor() {
        this.services = {
            capibara6Server: null,
            ollama: null,
            bbServer: null
        };
        this.ip = null;
    }

    async checkConnection(ip) {
        this.ip = ip;
        console.log(`🔍 Verificando conexión a VM bounty2: ${ip}`);
        
        // Comprobar conectividad general
        await this.checkConnectivity();
        
        // Intentar identificar servicios
        await this.identifyServices();
        
        // Mostrar resumen
        this.displayResults();
        
        return this.services;
    }

    async checkConnectivity() {
        console.log(`\n📡 Probando conectividad general...`);
        
        // Usamos un endpoint genérico para ver si la VM responde
        try {
            const response = await fetch(`http://${this.ip}`, { 
                method: 'HEAD',
                timeout: 5000
            });
            console.log(`✅ VM responde - Código: ${response.status}`);
        } catch (error) {
            console.log(`❌ No se puede conectar a la VM: ${error.message}`);
        }
    }

    async identifyServices() {
        console.log(`\n🔍 Identificando servicios activos...`);
        
        // Verificar posibles puertos según los procesos detectados
        const possiblePorts = [
            { port: 5001, name: 'Capibara6 Integrated Server', process: 'capibara6_integrated_server_ollama.py' },
            { port: 11434, name: 'Ollama', process: 'ollama serve' },
            { port: 3000, name: 'BB Server', process: 'node server.js' },
            { port: 8080, name: 'Web Server', process: 'python -m http.server' }
        ];

        for (const service of possiblePorts) {
            await this.checkService(service);
        }
    }

    async checkService(service) {
        try {
            console.log(`  Verificando ${service.name} en puerto ${service.port}...`);
            
            // Verificar si el puerto está abierto
            const signal = new AbortController();
            setTimeout(() => signal.abort(), 3000); // 3 segundos timeout
            
            const response = await fetch(`http://${this.ip}:${service.port}/health`, {
                signal: signal.signal,
                method: 'GET'
            }).catch(() => fetch(`http://${this.ip}:${service.port}/api/health`, {
                signal: signal.signal,
                method: 'GET'
            }));

            if (response.ok) {
                console.log(`  ✅ ${service.name} encontrado en puerto ${service.port}`);
                
                // Guardar información del servicio
                this.services[service.name.toLowerCase().replace(/\s+/g, '')] = {
                    port: service.port,
                    endpoint: `http://${this.ip}:${service.port}`,
                    process: service.process,
                    status: 'running',
                    response: response.status
                };
            } else {
                // Probar con otros endpoints comunes
                const endpointsToTry = ['', '/api', '/status', '/version'];
                let found = false;

                for (const endpoint of endpointsToTry) {
                    try {
                        const altResponse = await fetch(`http://${this.ip}:${service.port}${endpoint}`, {
                            signal: signal.signal,
                            method: 'GET'
                        });
                        if (altResponse.ok) {
                            console.log(`  ⚠️  ${service.name} responde en puerto ${service.port}${endpoint}`);
                            this.services[service.name.toLowerCase().replace(/\s+/g, '')] = {
                                port: service.port,
                                endpoint: `http://${this.ip}:${service.port}${endpoint}`,
                                process: service.process,
                                status: 'running',
                                response: altResponse.status
                            };
                            found = true;
                            break;
                        }
                    } catch (e) {
                        continue;
                    }
                }

                if (!found) {
                    console.log(`  ❌ ${service.name} no responde en puerto ${service.port}`);
                }
            }
        } catch (error) {
            console.log(`  ❌ ${service.name} no accesible en puerto ${service.port}: ${error.message}`);
        }
    }

    displayResults() {
        console.log(`\n📋 RESUMEN DE CONEXIÓN:`);
        console.log(`   VM bounty2: ${this.ip}`);
        console.log(`\n   Servicios identificados:`);
        
        let hasCapibara6 = false;
        for (const [serviceName, serviceInfo] of Object.entries(this.services)) {
            if (serviceInfo) {
                console.log(`     ✅ ${serviceName.toUpperCase()}: ${serviceInfo.endpoint} (puerto ${serviceInfo.port})`);
                if (serviceName.includes('capibara6')) {
                    hasCapibara6 = true;
                }
            }
        }

        if (!hasCapibara6) {
            console.log(`     ❌ No se encontró servidor Capibara6 activo`);
        }

        if (this.services.capibara6server) {
            console.log(`\n🎯 CONFIGURACIÓN RECOMENDADA PARA FRONTEND:`);
            console.log(`   BACKEND_URL: 'http://${this.ip}:${this.services.capibara6server.port}'`);
            console.log(`   Endpoint principal: ${this.services.capibara6server.endpoint}/api/chat`);
        }
    }

    // Método para generar configuración para el frontend
    generateFrontendConfig() {
        if (!this.services.capibara6server) {
            console.log('❌ No se puede generar configuración: Servidor Capibara6 no encontrado');
            return null;
        }

        const config = `
// Configuración generada automáticamente para conexión a VM bounty2
const GENERATED_CONFIG = {
    BACKEND_URL: 'http://${this.ip}:${this.services.capibara6server.port}',
    ENDPOINTS: {
        CHAT: '/api/chat',
        CHAT_STREAM: '/api/chat/stream',
        SAVE_CONVERSATION: '/api/save-conversation',
        SAVE_LEAD: '/api/save-lead',
        HEALTH: '/api/health',
        MCP_STATUS: '/api/mcp/status',
        MCP_TOOLS_CALL: '/api/mcp/tools/call'
    }
};

console.log('🔧 Configuración generada para VM bounty2 en ${this.ip}');
console.log('📡 Servicios detectados:');
${Object.entries(this.services)
    .filter(([_, info]) => info)
    .map(([name, info]) => `console.log('   ${name}: ${info.endpoint}');`)
    .join('\n')}
        `;
        
        return config;
    }
}

// Función para iniciar la comprobación
async function checkVMConnection(ip) {
    if (!ip) {
        console.error('❌ Debes proporcionar la IP pública de la VM bounty2');
        console.log('   Obtén la IP con: gcloud compute instances describe bounty2 --zone=europe-west4-a --project=mamba-001 --format="value(networkInterfaces[0].accessConfigs[0].natIP)"');
        return;
    }

    const checker = new VMConnectionChecker();
    return await checker.checkConnection(ip);
}

// Para usar: checkVMConnection('LA_IP_PUBLICA_DE_BOUNTY2');
console.log('💡 Para usar este checker: checkVMConnection(\'LA_IP_PUBLICA_DE_BOUNTY2\')');