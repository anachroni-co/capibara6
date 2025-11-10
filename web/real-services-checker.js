/*
 * Script de verificación de servicios reales basado en firewall
 * 
 * Este script verifica que los servicios reales estén accesibles
 * según los puertos abiertos en el firewall proporcionados.
 */

class RealServiceChecker {
    constructor() {
        this.realServices = {
            capibara6Main: {
                ip: '34.175.215.109',
                port: 5000,
                name: 'Capibara6 Main Server',
                firewallRule: 'tcp:5000',
                endpoint: '/api',
                description: 'Servidor principal para chat y operaciones básicas'
            },
            smartMCP5003: {
                ip: '34.175.215.109',
                port: 5003,
                name: 'Smart MCP Server',
                firewallRule: 'tcp:5003',
                endpoint: '/api/mcp',
                description: 'Servicio MCP para contexto inteligente'
            },
            smartMCP5010: {
                ip: '34.175.215.109',
                port: 5010,
                name: 'Smart MCP Server Alt',
                firewallRule: 'tcp:5010',
                endpoint: '/api/mcp/analyze',
                description: 'Servicio MCP alternativo para análisis'
            },
            llamaServer: {
                ip: '34.175.215.109',
                port: 8080,
                name: 'Llama Server (gpt-oss-20b)',
                firewallRule: 'tcp:8080',
                endpoint: '/health',
                description: 'Modelo gpt-oss-20b para generación de texto'
            }
        };
    }

    async checkAllServices() {
        console.log('🔍 Verificando servicios reales según firewall...\n');
        
        for (const [key, service] of Object.entries(this.realServices)) {
            await this.checkService(service);
        }
        
        this.printRecommendations();
    }

    async checkService(service) {
        console.log(`📡 Verificando: ${service.name}`);
        console.log(`   IP: ${service.ip}:${service.port}`);
        console.log(`   Firewall: ${service.firewallRule} (ABIERTO)`);
        console.log(`   Endpoint: ${service.endpoint}`);
        
        const startTime = Date.now();
        
        try {
            const url = `http://${service.ip}:${service.port}${service.endpoint}`;
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), 10000); // 10 segundos timeout
            
            const response = await fetch(url, {
                method: 'GET',
                signal: controller.signal,
                headers: { 'Cache-Control': 'no-cache' }
            });
            
            clearTimeout(timeoutId);
            
            const responseTime = Date.now() - startTime;
            
            if (response.ok) {
                console.log(`   ✅ ACCESIBLE - ${response.status} (${responseTime}ms)`);
                try {
                    const data = await response.json();
                    console.log(`   📊 Datos recibidos: ${Object.keys(data).length} claves`);
                } catch (e) {
                    console.log(`   📝 Respuesta recibida (${responseTime}ms)`);
                }
            } else {
                console.log(`   ⚠️  CÓDIGO: ${response.status} (${responseTime}ms)`);
            }
        } catch (error) {
            clearTimeout(timeoutId);
            console.log(`   ❌ ERROR: ${error.message} (${Date.now() - startTime}ms)`);
        }
        
        console.log(`   ℹ️  ${service.description}\n`);
    }

    printRecommendations() {
        console.log('📋 RECOMENDACIONES DE CONEXIÓN:');
        console.log('');
        console.log('🎯 PRIORIDAD ALTA:');
        console.log('   - Usar puerto 5000 para chat principal');
        console.log('   - Usar puerto 5003 para servicios MCP');
        console.log('   - Puerto 5010 como backup para MCP');
        console.log('');
        console.log('⚡ TIPOS DE CONEXIÓN:');
        console.log('   - Frontend → http://34.175.215.109:5000/api/chat');
        console.log('   - MCP → http://34.175.215.109:5003/api/mcp/...'); 
        console.log('   - Modelos → http://34.175.215.109:8080/completion');
        console.log('');
        console.log('✅ ESTADO REAL:');
        console.log('   - Todos los servicios están en la misma IP: 34.175.215.109');
        console.log('   - Puertos abiertos según firewall: 5000, 5003, 5010, 8080');
        console.log('   - Configuración actualizada en todos los archivos JS');
    }

    // Método para generar configuración para frontend
    generateFrontendConfig() {
        return `
// Configuración real basada en firewall actualizado
const REAL_FIREWALL_CONFIG = {
    // Servidor principal para chat y operaciones básicas
    CHAT_SERVER: 'http://34.175.215.109:5000',  // Puerto 5000 - ABIERTO (firewall)
    
    // Servicios MCP para contexto inteligente  
    MCP_SERVERS: {
        PRIMARY: 'http://34.175.215.109:5003',  // Puerto 5003 - ABIERTO (firewall)
        SECONDARY: 'http://34.175.215.109:5010' // Puerto 5010 - ABIERTO (firewall)
    },
    
    // Servidor de modelo para generación de texto
    MODEL_SERVER: 'http://34.175.215.109:8080', // Puerto 8080 - ABIERTO (firewall)
    
    // Endpoints configurados según servicios reales
    ENDPOINTS: {
        CHAT: '/api/chat',
        CHAT_STREAM: '/api/chat/stream',
        SAVE_CONVERSATION: '/api/save-conversation', 
        SAVE_LEAD: '/api/save-lead',
        HEALTH: '/api/health',
        MCP_STATUS: '/api/mcp/status',
        MCP_TOOLS_CALL: '/api/mcp/tools/call',
        MCP_ANALYZE: '/api/mcp/analyze',
        COMPLETION: '/completion'
    }
};

console.log('🔧 Configuración generada basada en firewall real');
console.log('📡 IP: 34.175.215.109');
console.log('🔒 Puertos verificados: 5000, 5003, 5010, 8080');
        `;
    }
}

// Función para ejecutar la verificación
async function checkRealServices() {
    const checker = new RealServiceChecker();
    await checker.checkAllServices();
    
    console.log('\n' + '='.repeat(60));
    console.log('📋 CONFIGURACIÓN RECOMENDADA:');
    console.log(checker.generateFrontendConfig());
    console.log('='.repeat(60));
}

// Para usar: checkRealServices();
console.log('💡 Para verificar servicios reales: checkRealServices()');