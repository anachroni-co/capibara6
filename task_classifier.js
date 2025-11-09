class CTMTaskClassifier {
  constructor() {
    // Contexto de memoria de trabajo (Working Memory)
    this.workingMemory = new Map();
    // Planificador de tareas jerárquico
    this.taskHierarchy = {
      'fast_response': { priority: 1, cognitiveLoad: 0.2 },
      'balanced': { priority: 2, cognitiveLoad: 0.5 },
      'complex': { priority: 3, cognitiveLoad: 0.8 }
    };
    // Historial de decisiones para aprendizaje contextual
    this.decisionHistory = [];
  }

  /**
   * Clasificación de tareas inspirada en CTM (Cognitively-Inspired Task Management)
   * Basado en los principios de planificación jerárquica, recursos atencionales y memoria
   */
  static classifyTask(prompt) {
    const classifier = new CTMTaskClassifier();
    return classifier.classifyWithCTM(prompt);
  }

  classifyWithCTM(prompt) {
    const promptLower = prompt.toLowerCase();
    
    // Fase 1: Análisis de atención selectiva (Selective Attention)
    const attentionFeatures = this.extractAttentionFeatures(promptLower);
    
    // Fase 2: Evaluación de recursos cognitivos necesarios
    const cognitiveLoad = this.estimateCognitiveLoad(prompt, attentionFeatures);
    
    // Fase 3: Planificación jerárquica basada en recursos disponibles
    const taskType = this.hierarchicalPlanning(cognitiveLoad, attentionFeatures);
    
    // Fase 4: Actualización de memoria de trabajo
    this.updateWorkingMemory(prompt, taskType, cognitiveLoad);
    
    return taskType;
  }

  /**
   * Fase 1: Análisis de características usando atención selectiva
   */
  extractAttentionFeatures(promptLower) {
    const features = {
      complexity: 0,
      contextDemand: 0,
      reasoningDepth: 0,
      creativeElements: 0,
      factualElements: 0
    };

    // Indicadores de complejidad (complexity)
    const complexityIndicators = [
      'análisis', 'razonamiento', 'comparación', 'evaluar', 'estrategia', 
      'planificación', 'investigación', 'profundo', 'detalle', 'complejo', 
      'técnico', 'evaluación', 'interpretación', 'síntesis', 'problema', 
      'dilema', 'paradigma', 'metodología', 'hipótesis', 'teoría'
    ];
    
    // Indicadores de demanda de contexto (contextDemand)  
    const contextIndicators = [
      'contexto', 'relevancia', 'antecedentes', 'implicaciones', 
      'relación con', 'conexión entre', 'trasfondo', 'marco', 
      'entorno', 'escenario', 'situación', 'caso práctico'
    ];
    
    // Indicadores de profundidad de razonamiento (reasoningDepth)
    const reasoningIndicators = [
      'por qué', 'cuál es la causa', 'qué implica', 'cómo se relaciona', 
      'qué consecuencias', 'qué factores', 'qué variables', 'qué aspectos', 
      'qué dimensión', 'qué perspectiva', 'qué ángulo', 'desde qué punto de vista'
    ];
    
    // Indicadores de elementos creativos (creativeElements)
    const creativeIndicators = [
      'crea', 'inventa', 'diseña', 'propón', 'imagina', 'ficción', 
      'escribe historia', 'narrativa', 'poesía', 'metáfora', 'analogía', 
      'relato', 'cuento', 'escenario', 'posible solución'
    ];
    
    // Indicadores de elementos factuales (factualElements)
    const factualIndicators = [
      'qué', 'quién', 'cuál', 'cuándo', 'dónde', 'definir', 'qué es', 
      'cuánto', 'cantidad', 'dato', 'hecho', 'información', 'nombre', 
      'concepto', 'significado', 'chiste', 'broma', 'saludo', 'ayuda'
    ];

    // Contar indicadores de cada tipo
    complexityIndicators.forEach(indicator => {
      if (promptLower.includes(indicator)) features.complexity += 2;
    });

    contextIndicators.forEach(indicator => {
      if (promptLower.includes(indicator)) features.contextDemand += 1;
    });

    reasoningIndicators.forEach(indicator => {
      if (promptLower.includes(indicator)) features.reasoningDepth += 1;
    });

    creativeIndicators.forEach(indicator => {
      if (promptLower.includes(indicator)) features.creativeElements += 1;
    });

    factualIndicators.forEach(indicator => {
      if (promptLower.includes(indicator)) features.factualElements += 1;
    });

    return features;
  }

  /**
   * Fase 2: Estimación de carga cognitiva
   */
  estimateCognitiveLoad(prompt, features) {
    let cognitiveLoad = 0;
    
    // Ponderaciones basadas en la importancia de cada característica
    cognitiveLoad += features.complexity * 0.4;      // Alta ponderación
    cognitiveLoad += features.contextDemand * 0.2;    // Media ponderación
    cognitiveLoad += features.reasoningDepth * 0.3;   // Alta ponderación
    cognitiveLoad += features.creativeElements * 0.25; // Media-alta ponderación
    cognitiveLoad += features.factualElements * 0.1;  // Baja ponderación
    
    // Considerar la longitud del prompt
    if (prompt.length > 100) cognitiveLoad += 0.1;
    if (prompt.length > 200) cognitiveLoad += 0.2;
    
    // Considerar la complejidad sintáctica (número de frases)
    const sentenceCount = prompt.split(/[.!?]+/).filter(s => s.trim().length > 0).length;
    if (sentenceCount > 3) cognitiveLoad += 0.1;
    
    // Normalizar la carga cognitiva a un rango de 0 a 1
    cognitiveLoad = Math.min(cognitiveLoad, 1.0);
    
    return cognitiveLoad;
  }

  /**
   * Fase 3: Planificación jerárquica
   */
  hierarchicalPlanning(cognitiveLoad, features) {
    // Definir umbrales de carga cognitiva para cada tipo de tarea
    if (cognitiveLoad > 0.65) {
      // Tarea compleja basada en carga cognitiva
      return 'complex';
    } else if (cognitiveLoad > 0.3) {
      // Evaluación adicional basada en características específicas
      if (features.reasoningDepth > 2 || features.complexity > 4 || features.contextDemand > 2) {
        return 'complex';
      } else if (features.creativeElements > 1) {
        // Las tareas creativas suelen requerir un modelo equilibrado
        return 'balanced';
      } else {
        return 'balanced';
      }
    } else {
      // Tareas simples basadas en carga cognitiva baja
      if (features.factualElements > 3) {
        // Muchas preguntas factuales pueden ser complejas
        return 'balanced';
      } else {
        return 'fast_response';
      }
    }
  }

  /**
   * Fase 4: Actualizar memoria de trabajo
   */
  updateWorkingMemory(prompt, taskType, cognitiveLoad) {
    // Registrar la decisión para futuras referencias
    this.decisionHistory.push({
      prompt: prompt.substring(0, 100) + '...', // Tomar solo los primeros 100 caracteres
      taskType,
      cognitiveLoad,
      timestamp: Date.now()
    });
    
    // Mantener solo las últimas 50 decisiones para no sobrecargar la memoria
    if (this.decisionHistory.length > 50) {
      this.decisionHistory.shift();
    }
  }

  static estimateResponseTime(modelTier) {
    const responseTimes = {
      'fast_response': 2000,    // ~2 segundos
      'balanced': 4000,         // ~4 segundos
      'complex': 120000         // ~2 minutos
    };
    return responseTimes[modelTier];
  }
  
  /**
   * Obtener estadísticas de la memoria de trabajo
   */
  getWorkingMemoryStats() {
    const stats = {
      totalDecisions: this.decisionHistory.length,
      taskTypeDistribution: {},
      averageCognitiveLoad: 0
    };
    
    this.decisionHistory.forEach(decision => {
      if (!stats.taskTypeDistribution[decision.taskType]) {
        stats.taskTypeDistribution[decision.taskType] = 0;
      }
      stats.taskTypeDistribution[decision.taskType]++;
    });
    
    if (this.decisionHistory.length > 0) {
      const totalLoad = this.decisionHistory.reduce((sum, decision) => sum + decision.cognitiveLoad, 0);
      stats.averageCognitiveLoad = totalLoad / this.decisionHistory.length;
    }
    
    return stats;
  }
}

// Mantener compatibilidad con la interfaz anterior
class TaskClassifier {
  static classifyTask(prompt) {
    return CTMTaskClassifier.classifyTask(prompt);
  }

  static estimateResponseTime(modelTier) {
    return CTMTaskClassifier.estimateResponseTime(modelTier);
  }
}

// Exportar las clases para que sean utilizables en otros módulos
module.exports = { TaskClassifier, CTMTaskClassifier };