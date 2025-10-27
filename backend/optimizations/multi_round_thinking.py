#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Multi-round Thinking - Sistema de razonamiento iterativo y reflexión.
"""

import logging
import json
import os
import time
from typing import Dict, List, Any, Optional, Tuple, Union
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum
from collections import defaultdict, deque
import numpy as np

logger = logging.getLogger(__name__)


class ThinkingMode(Enum):
    """Modos de pensamiento."""
    ANALYTICAL = "analytical"
    CREATIVE = "creative"
    CRITICAL = "critical"
    INTUITIVE = "intuitive"
    SYSTEMATIC = "systematic"
    ADAPTIVE = "adaptive"


class ReasoningType(Enum):
    """Tipos de razonamiento."""
    DEDUCTIVE = "deductive"
    INDUCTIVE = "inductive"
    ABDUCTIVE = "abductive"
    ANALOGICAL = "analogical"
    CAUSAL = "causal"
    COUNTERFACTUAL = "counterfactual"


class ConfidenceLevel(Enum):
    """Niveles de confianza."""
    VERY_LOW = 1
    LOW = 2
    MEDIUM = 3
    HIGH = 4
    VERY_HIGH = 5


@dataclass
class ThinkingStep:
    """Paso de pensamiento."""
    step_id: str
    thinking_mode: ThinkingMode
    reasoning_type: ReasoningType
    input_context: str
    thought_content: str
    confidence_level: ConfidenceLevel
    reasoning_chain: List[str]
    assumptions: List[str]
    evidence: List[str]
    alternatives: List[str]
    timestamp: datetime
    metadata: Dict[str, Any]


@dataclass
class ThinkingRound:
    """Ronda de pensamiento."""
    round_id: str
    round_number: int
    steps: List[ThinkingStep]
    synthesis: str
    confidence_score: float
    quality_score: float
    insights: List[str]
    questions_raised: List[str]
    next_directions: List[str]
    timestamp: datetime
    duration_seconds: float


@dataclass
class ThinkingSession:
    """Sesión de pensamiento."""
    session_id: str
    initial_query: str
    rounds: List[ThinkingRound]
    final_conclusion: str
    overall_confidence: float
    overall_quality: float
    total_duration_seconds: float
    thinking_modes_used: List[ThinkingMode]
    reasoning_types_used: List[ReasoningType]
    created_at: datetime
    completed_at: Optional[datetime]
    metadata: Dict[str, Any]


@dataclass
class ThinkingPrompt:
    """Prompt de pensamiento."""
    prompt_id: str
    thinking_mode: ThinkingMode
    reasoning_type: ReasoningType
    prompt_template: str
    variables: List[str]
    expected_output_format: str
    quality_criteria: List[str]


class ThinkingEngine:
    """Motor de pensamiento."""
    
    def __init__(self):
        self.thinking_prompts = self._initialize_thinking_prompts()
        self.reasoning_patterns = self._initialize_reasoning_patterns()
        
        # Estadísticas
        self.thinking_stats = {
            'total_sessions': 0,
            'total_rounds': 0,
            'total_steps': 0,
            'average_confidence': 0.0,
            'average_quality': 0.0,
            'thinking_mode_usage': defaultdict(int),
            'reasoning_type_usage': defaultdict(int)
        }
        
        logger.info("ThinkingEngine inicializado")
    
    def _initialize_thinking_prompts(self) -> Dict[str, ThinkingPrompt]:
        """Inicializa prompts de pensamiento."""
        prompts = {}
        
        # Prompt analítico
        prompts['analytical'] = ThinkingPrompt(
            prompt_id="analytical",
            thinking_mode=ThinkingMode.ANALYTICAL,
            reasoning_type=ReasoningType.DEDUCTIVE,
            prompt_template="Analiza {query} de manera sistemática. Descompón el problema en componentes más pequeños y examina cada uno cuidadosamente. ¿Qué patrones puedes identificar? ¿Qué datos son relevantes?",
            variables=["query"],
            expected_output_format="Análisis estructurado con componentes identificados",
            quality_criteria=["claridad", "completitud", "estructura"]
        )
        
        # Prompt creativo
        prompts['creative'] = ThinkingPrompt(
            prompt_id="creative",
            thinking_mode=ThinkingMode.CREATIVE,
            reasoning_type=ReasoningType.ANALOGICAL,
            prompt_template="Piensa creativamente sobre {query}. ¿Qué enfoques inusuales o innovadores podrías considerar? ¿Qué analogías o metáforas podrían ser útiles? ¿Qué ideas completamente nuevas surgen?",
            variables=["query"],
            expected_output_format="Ideas creativas e innovadoras",
            quality_criteria=["originalidad", "innovación", "viabilidad"]
        )
        
        # Prompt crítico
        prompts['critical'] = ThinkingPrompt(
            prompt_id="critical",
            thinking_mode=ThinkingMode.CRITICAL,
            reasoning_type=ReasoningType.COUNTERFACTUAL,
            prompt_template="Evalúa críticamente {query}. ¿Qué suposiciones están siendo hechas? ¿Qué evidencia falta? ¿Qué contraargumentos podrían existir? ¿Dónde podrían estar los puntos débiles?",
            variables=["query"],
            expected_output_format="Evaluación crítica con contraargumentos",
            quality_criteria=["rigor", "escepticismo", "evidencia"]
        )
        
        # Prompt intuitivo
        prompts['intuitive'] = ThinkingPrompt(
            prompt_id="intuitive",
            thinking_mode=ThinkingMode.INTUITIVE,
            reasoning_type=ReasoningType.ABDUCTIVE,
            prompt_template="Usa tu intuición para abordar {query}. ¿Qué te dice tu instinto? ¿Qué sensaciones o impresiones tienes? ¿Qué conexiones sientes que podrían no ser obvias?",
            variables=["query"],
            expected_output_format="Insights intuitivos y conexiones",
            quality_criteria=["intuición", "conexiones", "perspicacia"]
        )
        
        # Prompt sistemático
        prompts['systematic'] = ThinkingPrompt(
            prompt_id="systematic",
            thinking_mode=ThinkingMode.SYSTEMATIC,
            reasoning_type=ReasoningType.CAUSAL,
            prompt_template="Aborda {query} de manera sistemática. ¿Cuáles son las causas y efectos? ¿Cómo se relacionan los diferentes elementos? ¿Qué secuencia lógica sigue el proceso?",
            variables=["query"],
            expected_output_format="Análisis sistemático con relaciones causales",
            quality_criteria=["sistematicidad", "lógica", "completitud"]
        )
        
        return prompts
    
    def _initialize_reasoning_patterns(self) -> Dict[ReasoningType, List[str]]:
        """Inicializa patrones de razonamiento."""
        return {
            ReasoningType.DEDUCTIVE: [
                "Si A entonces B, A es verdadero, por tanto B es verdadero",
                "Todos los X son Y, Z es X, por tanto Z es Y",
                "La regla general es R, este caso sigue la regla, por tanto la conclusión es C"
            ],
            ReasoningType.INDUCTIVE: [
                "Observo que X1, X2, X3 tienen la propiedad P, por tanto probablemente todos los X tienen P",
                "En los casos estudiados, siempre ocurre Y cuando X, por tanto probablemente Y ocurre cuando X",
                "La evidencia sugiere que Z es verdadero en estos casos, por tanto probablemente Z es verdadero en general"
            ],
            ReasoningType.ABDUCTIVE: [
                "Observo el fenómeno P, la mejor explicación es H, por tanto probablemente H es verdadero",
                "Los datos D son consistentes con la hipótesis H, por tanto H es una explicación plausible",
                "Si H fuera verdadero, explicaría los hechos observados, por tanto H es probable"
            ],
            ReasoningType.ANALOGICAL: [
                "X es como Y en aspectos A, B, C, Y tiene propiedad P, por tanto X probablemente tiene P",
                "La situación S es similar a la situación T, T resultó en R, por tanto S probablemente resultará en R",
                "El problema P es análogo al problema Q, Q se resolvió con método M, por tanto P podría resolverse con M"
            ],
            ReasoningType.CAUSAL: [
                "A causa B, B causa C, por tanto A causa C",
                "Cuando A ocurre, B siempre sigue, por tanto A es causa de B",
                "La eliminación de A elimina B, por tanto A es necesario para B"
            ],
            ReasoningType.COUNTERFACTUAL: [
                "Si A no hubiera ocurrido, entonces B no habría ocurrido",
                "En ausencia de X, Y habría sido diferente",
                "Si las condiciones hubieran sido C en lugar de D, el resultado habría sido E"
            ]
        }
    
    def generate_thinking_step(self, 
                             query: str,
                             thinking_mode: ThinkingMode,
                             reasoning_type: ReasoningType,
                             context: str = "") -> ThinkingStep:
        """Genera paso de pensamiento."""
        try:
            step_id = f"step_{int(time.time() * 1000)}"
            
            # Obtener prompt apropiado
            prompt = self._get_prompt_for_mode(thinking_mode)
            
            # Generar contenido de pensamiento
            thought_content = self._generate_thought_content(query, prompt, context)
            
            # Generar cadena de razonamiento
            reasoning_chain = self._generate_reasoning_chain(reasoning_type, thought_content)
            
            # Identificar suposiciones
            assumptions = self._identify_assumptions(thought_content)
            
            # Identificar evidencia
            evidence = self._identify_evidence(thought_content)
            
            # Generar alternativas
            alternatives = self._generate_alternatives(thought_content, reasoning_type)
            
            # Calcular nivel de confianza
            confidence_level = self._calculate_confidence_level(thought_content, evidence, assumptions)
            
            step = ThinkingStep(
                step_id=step_id,
                thinking_mode=thinking_mode,
                reasoning_type=reasoning_type,
                input_context=context,
                thought_content=thought_content,
                confidence_level=confidence_level,
                reasoning_chain=reasoning_chain,
                assumptions=assumptions,
                evidence=evidence,
                alternatives=alternatives,
                timestamp=datetime.now(),
                metadata={'generated_by': 'thinking_engine'}
            )
            
            # Actualizar estadísticas
            self.thinking_stats['total_steps'] += 1
            self.thinking_stats['thinking_mode_usage'][thinking_mode.value] += 1
            self.thinking_stats['reasoning_type_usage'][reasoning_type.value] += 1
            
            logger.info(f"Paso de pensamiento generado: {step_id} ({thinking_mode.value})")
            return step
            
        except Exception as e:
            logger.error(f"Error generando paso de pensamiento: {e}")
            return self._create_fallback_step(query, thinking_mode, reasoning_type)
    
    def _get_prompt_for_mode(self, thinking_mode: ThinkingMode) -> ThinkingPrompt:
        """Obtiene prompt para modo de pensamiento."""
        mode_prompts = {
            ThinkingMode.ANALYTICAL: 'analytical',
            ThinkingMode.CREATIVE: 'creative',
            ThinkingMode.CRITICAL: 'critical',
            ThinkingMode.INTUITIVE: 'intuitive',
            ThinkingMode.SYSTEMATIC: 'systematic'
        }
        
        prompt_key = mode_prompts.get(thinking_mode, 'analytical')
        return self.thinking_prompts[prompt_key]
    
    def _generate_thought_content(self, query: str, prompt: ThinkingPrompt, context: str) -> str:
        """Genera contenido de pensamiento."""
        # Implementación simplificada - en producción usaría un modelo de lenguaje
        template = prompt.prompt_template
        formatted_prompt = template.format(query=query)
        
        # Simular generación de contenido
        if prompt.thinking_mode == ThinkingMode.ANALYTICAL:
            content = f"Análisis de '{query}': Descomponiendo el problema en componentes clave. Identificando patrones y relaciones. Evaluando evidencia disponible."
        elif prompt.thinking_mode == ThinkingMode.CREATIVE:
            content = f"Enfoque creativo para '{query}': Explorando ideas innovadoras. Considerando analogías y metáforas. Generando soluciones no convencionales."
        elif prompt.thinking_mode == ThinkingMode.CRITICAL:
            content = f"Evaluación crítica de '{query}': Examinando suposiciones subyacentes. Identificando limitaciones y sesgos. Considerando contraargumentos."
        elif prompt.thinking_mode == ThinkingMode.INTUITIVE:
            content = f"Perspectiva intuitiva sobre '{query}': Siguiendo instintos y sensaciones. Reconociendo patrones sutiles. Conectando ideas aparentemente no relacionadas."
        elif prompt.thinking_mode == ThinkingMode.SYSTEMATIC:
            content = f"Análisis sistemático de '{query}': Mapeando relaciones causales. Siguiendo secuencias lógicas. Considerando el sistema completo."
        else:
            content = f"Reflexión sobre '{query}': Considerando múltiples perspectivas. Integrando diferentes enfoques. Buscando síntesis."
        
        if context:
            content += f"\n\nContexto adicional: {context}"
        
        return content
    
    def _generate_reasoning_chain(self, reasoning_type: ReasoningType, thought_content: str) -> List[str]:
        """Genera cadena de razonamiento."""
        patterns = self.reasoning_patterns.get(reasoning_type, [])
        
        # Seleccionar patrón apropiado
        if patterns:
            selected_pattern = patterns[0]  # Simplificado
            return [selected_pattern, f"Aplicando este patrón a: {thought_content[:100]}..."]
        else:
            return [f"Razonamiento {reasoning_type.value}: {thought_content[:100]}..."]
    
    def _identify_assumptions(self, thought_content: str) -> List[str]:
        """Identifica suposiciones en el pensamiento."""
        # Implementación simplificada - en producción usaría NLP
        assumptions = []
        
        # Buscar palabras clave que indican suposiciones
        assumption_keywords = ["asumiendo", "suponiendo", "si", "cuando", "dado que"]
        
        for keyword in assumption_keywords:
            if keyword in thought_content.lower():
                assumptions.append(f"Suposición implícita relacionada con '{keyword}'")
        
        if not assumptions:
            assumptions.append("Suposición implícita sobre la validez del enfoque")
        
        return assumptions
    
    def _identify_evidence(self, thought_content: str) -> List[str]:
        """Identifica evidencia en el pensamiento."""
        # Implementación simplificada
        evidence = []
        
        # Buscar palabras clave que indican evidencia
        evidence_keywords = ["evidencia", "datos", "hechos", "observación", "resultado"]
        
        for keyword in evidence_keywords:
            if keyword in thought_content.lower():
                evidence.append(f"Evidencia mencionada relacionada con '{keyword}'")
        
        if not evidence:
            evidence.append("Evidencia implícita en el razonamiento")
        
        return evidence
    
    def _generate_alternatives(self, thought_content: str, reasoning_type: ReasoningType) -> List[str]:
        """Genera alternativas al pensamiento."""
        alternatives = []
        
        if reasoning_type == ReasoningType.DEDUCTIVE:
            alternatives.append("Considerar si las premisas son realmente verdaderas")
            alternatives.append("Evaluar si la lógica es válida")
        elif reasoning_type == ReasoningType.INDUCTIVE:
            alternatives.append("Considerar si la muestra es representativa")
            alternatives.append("Evaluar si hay excepciones importantes")
        elif reasoning_type == ReasoningType.ABDUCTIVE:
            alternatives.append("Considerar otras explicaciones posibles")
            alternatives.append("Evaluar si la explicación es la más simple")
        else:
            alternatives.append("Considerar enfoques alternativos")
            alternatives.append("Evaluar perspectivas diferentes")
        
        return alternatives
    
    def _calculate_confidence_level(self, thought_content: str, evidence: List[str], assumptions: List[str]) -> ConfidenceLevel:
        """Calcula nivel de confianza."""
        # Factores que aumentan confianza
        evidence_score = len(evidence) * 0.3
        content_length_score = min(1.0, len(thought_content) / 500) * 0.2
        
        # Factores que disminuyen confianza
        assumption_penalty = len(assumptions) * 0.1
        
        # Calcular score total
        total_score = evidence_score + content_length_score - assumption_penalty
        
        # Mapear a nivel de confianza
        if total_score >= 0.8:
            return ConfidenceLevel.VERY_HIGH
        elif total_score >= 0.6:
            return ConfidenceLevel.HIGH
        elif total_score >= 0.4:
            return ConfidenceLevel.MEDIUM
        elif total_score >= 0.2:
            return ConfidenceLevel.LOW
        else:
            return ConfidenceLevel.VERY_LOW
    
    def _create_fallback_step(self, query: str, thinking_mode: ThinkingMode, reasoning_type: ReasoningType) -> ThinkingStep:
        """Crea paso de fallback."""
        return ThinkingStep(
            step_id=f"fallback_{int(time.time() * 1000)}",
            thinking_mode=thinking_mode,
            reasoning_type=reasoning_type,
            input_context="",
            thought_content=f"Reflexión básica sobre: {query}",
            confidence_level=ConfidenceLevel.LOW,
            reasoning_chain=["Razonamiento simplificado"],
            assumptions=["Suposición básica"],
            evidence=["Evidencia limitada"],
            alternatives=["Enfoque alternativo"],
            timestamp=datetime.now(),
            metadata={'fallback': True}
        )


class MultiRoundThinking:
    """Sistema de pensamiento multi-ronda."""
    
    def __init__(self, 
                 max_rounds: int = 5,
                 min_confidence_threshold: float = 0.7,
                 thinking_engine: Optional[ThinkingEngine] = None):
        self.max_rounds = max_rounds
        self.min_confidence_threshold = min_confidence_threshold
        self.thinking_engine = thinking_engine or ThinkingEngine()
        
        # Sesiones activas
        self.active_sessions: Dict[str, ThinkingSession] = {}
        
        # Historial de sesiones
        self.session_history: deque = deque(maxlen=1000)
        
        # Estadísticas
        self.multi_round_stats = {
            'total_sessions': 0,
            'completed_sessions': 0,
            'average_rounds_per_session': 0.0,
            'average_session_duration_seconds': 0.0,
            'confidence_improvement_rate': 0.0,
            'quality_improvement_rate': 0.0
        }
        
        logger.info(f"MultiRoundThinking inicializado: max_rounds={max_rounds}")
    
    def start_thinking_session(self, 
                             query: str,
                             initial_context: str = "",
                             target_confidence: float = 0.8) -> str:
        """Inicia sesión de pensamiento."""
        try:
            session_id = f"session_{int(time.time() * 1000)}"
            
            # Crear sesión
            session = ThinkingSession(
                session_id=session_id,
                initial_query=query,
                rounds=[],
                final_conclusion="",
                overall_confidence=0.0,
                overall_quality=0.0,
                total_duration_seconds=0.0,
                thinking_modes_used=[],
                reasoning_types_used=[],
                created_at=datetime.now(),
                completed_at=None,
                metadata={
                    'target_confidence': target_confidence,
                    'initial_context': initial_context
                }
            )
            
            self.active_sessions[session_id] = session
            self.multi_round_stats['total_sessions'] += 1
            
            logger.info(f"Sesión de pensamiento iniciada: {session_id}")
            return session_id
            
        except Exception as e:
            logger.error(f"Error iniciando sesión de pensamiento: {e}")
            return ""
    
    def execute_thinking_round(self, 
                             session_id: str,
                             thinking_mode: ThinkingMode = ThinkingMode.ADAPTIVE,
                             reasoning_type: ReasoningType = ReasoningType.DEDUCTIVE) -> Optional[ThinkingRound]:
        """Ejecuta ronda de pensamiento."""
        try:
            if session_id not in self.active_sessions:
                logger.error(f"Sesión no encontrada: {session_id}")
                return None
            
            session = self.active_sessions[session_id]
            
            # Verificar límite de rondas
            if len(session.rounds) >= self.max_rounds:
                logger.warning(f"Límite de rondas alcanzado para sesión: {session_id}")
                return None
            
            round_number = len(session.rounds) + 1
            round_id = f"{session_id}_round_{round_number}"
            
            start_time = datetime.now()
            
            # Determinar modo de pensamiento si es adaptativo
            if thinking_mode == ThinkingMode.ADAPTIVE:
                thinking_mode = self._select_adaptive_mode(session)
            
            # Generar pasos de pensamiento
            steps = self._generate_thinking_steps(session, thinking_mode, reasoning_type)
            
            # Sintetizar la ronda
            synthesis = self._synthesize_round(steps, session)
            
            # Calcular métricas de la ronda
            confidence_score = self._calculate_round_confidence(steps)
            quality_score = self._calculate_round_quality(steps, synthesis)
            
            # Generar insights y preguntas
            insights = self._extract_insights(steps)
            questions_raised = self._generate_questions(steps, session)
            next_directions = self._suggest_next_directions(steps, session)
            
            # Crear ronda
            round_duration = (datetime.now() - start_time).total_seconds()
            
            thinking_round = ThinkingRound(
                round_id=round_id,
                round_number=round_number,
                steps=steps,
                synthesis=synthesis,
                confidence_score=confidence_score,
                quality_score=quality_score,
                insights=insights,
                questions_raised=questions_raised,
                next_directions=next_directions,
                timestamp=datetime.now(),
                duration_seconds=round_duration
            )
            
            # Agregar a la sesión
            session.rounds.append(thinking_round)
            session.thinking_modes_used.append(thinking_mode)
            session.reasoning_types_used.append(reasoning_type)
            
            # Actualizar estadísticas
            self.multi_round_stats['average_rounds_per_session'] = (
                (self.multi_round_stats['average_rounds_per_session'] * (self.multi_round_stats['total_sessions'] - 1) + 
                 len(session.rounds)) / self.multi_round_stats['total_sessions']
            )
            
            logger.info(f"Ronda de pensamiento completada: {round_id} (confianza: {confidence_score:.2f})")
            return thinking_round
            
        except Exception as e:
            logger.error(f"Error ejecutando ronda de pensamiento: {e}")
            return None
    
    def _select_adaptive_mode(self, session: ThinkingSession) -> ThinkingMode:
        """Selecciona modo de pensamiento adaptativo."""
        if not session.rounds:
            return ThinkingMode.ANALYTICAL  # Empezar con análisis
        
        last_round = session.rounds[-1]
        
        # Si la confianza es baja, usar pensamiento crítico
        if last_round.confidence_score < 0.5:
            return ThinkingMode.CRITICAL
        
        # Si la calidad es baja, usar pensamiento creativo
        if last_round.quality_score < 0.6:
            return ThinkingMode.CREATIVE
        
        # Si ya se han usado varios modos, usar síntesis
        if len(set(session.thinking_modes_used)) >= 3:
            return ThinkingMode.SYSTEMATIC
        
        # Rotar entre modos
        modes = [ThinkingMode.ANALYTICAL, ThinkingMode.CREATIVE, ThinkingMode.CRITICAL, ThinkingMode.INTUITIVE]
        used_modes = set(session.thinking_modes_used)
        available_modes = [mode for mode in modes if mode not in used_modes]
        
        return available_modes[0] if available_modes else ThinkingMode.SYSTEMATIC
    
    def _generate_thinking_steps(self, 
                               session: ThinkingSession, 
                               thinking_mode: ThinkingMode,
                               reasoning_type: ReasoningType) -> List[ThinkingStep]:
        """Genera pasos de pensamiento para la ronda."""
        steps = []
        
        # Contexto de la sesión
        context = session.initial_query
        if session.rounds:
            last_synthesis = session.rounds[-1].synthesis
            context += f"\n\nContexto de ronda anterior: {last_synthesis}"
        
        # Generar 2-3 pasos por ronda
        num_steps = min(3, max(2, len(session.rounds) + 1))
        
        for i in range(num_steps):
            step = self.thinking_engine.generate_thinking_step(
                session.initial_query,
                thinking_mode,
                reasoning_type,
                context
            )
            steps.append(step)
            
            # Actualizar contexto para siguiente paso
            context += f"\n\nPaso {i+1}: {step.thought_content[:200]}..."
        
        return steps
    
    def _synthesize_round(self, steps: List[ThinkingStep], session: ThinkingSession) -> str:
        """Sintetiza una ronda de pensamiento."""
        if not steps:
            return "No se generaron pasos de pensamiento."
        
        # Combinar contenido de los pasos
        combined_content = []
        for i, step in enumerate(steps, 1):
            combined_content.append(f"Paso {i} ({step.thinking_mode.value}): {step.thought_content}")
        
        # Crear síntesis
        synthesis = f"Síntesis de la ronda:\n\n" + "\n\n".join(combined_content)
        
        # Agregar insights clave
        key_insights = []
        for step in steps:
            if step.confidence_level.value >= ConfidenceLevel.HIGH.value:
                key_insights.append(step.thought_content[:100] + "...")
        
        if key_insights:
            synthesis += f"\n\nInsights clave: " + "; ".join(key_insights)
        
        return synthesis
    
    def _calculate_round_confidence(self, steps: List[ThinkingStep]) -> float:
        """Calcula confianza de la ronda."""
        if not steps:
            return 0.0
        
        # Promedio de confianza de los pasos
        total_confidence = sum(step.confidence_level.value for step in steps)
        average_confidence = total_confidence / len(steps)
        
        # Normalizar a 0-1
        return average_confidence / 5.0
    
    def _calculate_round_quality(self, steps: List[ThinkingStep], synthesis: str) -> float:
        """Calcula calidad de la ronda."""
        if not steps:
            return 0.0
        
        # Factores de calidad
        step_diversity = len(set(step.thinking_mode for step in steps)) / len(ThinkingMode)
        content_richness = min(1.0, len(synthesis) / 1000)
        evidence_quality = sum(len(step.evidence) for step in steps) / len(steps) / 3.0
        
        # Combinar factores
        quality = (step_diversity * 0.3 + 
                  content_richness * 0.4 + 
                  evidence_quality * 0.3)
        
        return min(1.0, quality)
    
    def _extract_insights(self, steps: List[ThinkingStep]) -> List[str]:
        """Extrae insights de los pasos."""
        insights = []
        
        for step in steps:
            if step.confidence_level.value >= ConfidenceLevel.MEDIUM.value:
                # Extraer insights de contenido de alta confianza
                content = step.thought_content
                if len(content) > 50:
                    insights.append(content[:150] + "...")
        
        return insights[:5]  # Limitar a 5 insights
    
    def _generate_questions(self, steps: List[ThinkingStep], session: ThinkingSession) -> List[str]:
        """Genera preguntas basadas en los pasos."""
        questions = []
        
        for step in steps:
            # Generar preguntas basadas en alternativas
            for alternative in step.alternatives:
                questions.append(f"¿Qué pasaría si {alternative.lower()}?")
            
            # Generar preguntas basadas en suposiciones
            for assumption in step.assumptions:
                questions.append(f"¿Es válida la suposición de que {assumption.lower()}?")
        
        return questions[:5]  # Limitar a 5 preguntas
    
    def _suggest_next_directions(self, steps: List[ThinkingStep], session: ThinkingSession) -> List[str]:
        """Sugiere próximas direcciones."""
        directions = []
        
        # Basado en insights
        insights = self._extract_insights(steps)
        for insight in insights:
            directions.append(f"Explorar más a fondo: {insight[:50]}...")
        
        # Basado en preguntas
        questions = self._generate_questions(steps, session)
        for question in questions:
            directions.append(f"Investigar: {question}")
        
        # Basado en modos de pensamiento no usados
        used_modes = set(session.thinking_modes_used)
        available_modes = [mode for mode in ThinkingMode if mode not in used_modes]
        if available_modes:
            directions.append(f"Probar enfoque {available_modes[0].value}")
        
        return directions[:3]  # Limitar a 3 direcciones
    
    def complete_thinking_session(self, session_id: str) -> Optional[ThinkingSession]:
        """Completa sesión de pensamiento."""
        try:
            if session_id not in self.active_sessions:
                logger.error(f"Sesión no encontrada: {session_id}")
                return None
            
            session = self.active_sessions[session_id]
            
            # Generar conclusión final
            session.final_conclusion = self._generate_final_conclusion(session)
            
            # Calcular métricas finales
            session.overall_confidence = self._calculate_overall_confidence(session)
            session.overall_quality = self._calculate_overall_quality(session)
            
            # Calcular duración total
            session.total_duration_seconds = (datetime.now() - session.created_at).total_seconds()
            session.completed_at = datetime.now()
            
            # Mover a historial
            self.session_history.append(session)
            del self.active_sessions[session_id]
            
            # Actualizar estadísticas
            self.multi_round_stats['completed_sessions'] += 1
            
            logger.info(f"Sesión de pensamiento completada: {session_id}")
            return session
            
        except Exception as e:
            logger.error(f"Error completando sesión de pensamiento: {e}")
            return None
    
    def _generate_final_conclusion(self, session: ThinkingSession) -> str:
        """Genera conclusión final de la sesión."""
        if not session.rounds:
            return "No se completaron rondas de pensamiento."
        
        # Combinar síntesis de todas las rondas
        round_syntheses = [round.synthesis for round in session.rounds]
        
        # Crear conclusión
        conclusion = f"Conclusión final sobre '{session.initial_query}':\n\n"
        
        for i, synthesis in enumerate(round_syntheses, 1):
            conclusion += f"Ronda {i}:\n{synthesis}\n\n"
        
        # Agregar insights finales
        all_insights = []
        for round in session.rounds:
            all_insights.extend(round.insights)
        
        if all_insights:
            conclusion += f"Insights finales: {'; '.join(all_insights[:5])}"
        
        return conclusion
    
    def _calculate_overall_confidence(self, session: ThinkingSession) -> float:
        """Calcula confianza general de la sesión."""
        if not session.rounds:
            return 0.0
        
        # Promedio de confianza de las rondas
        total_confidence = sum(round.confidence_score for round in session.rounds)
        return total_confidence / len(session.rounds)
    
    def _calculate_overall_quality(self, session: ThinkingSession) -> float:
        """Calcula calidad general de la sesión."""
        if not session.rounds:
            return 0.0
        
        # Factores de calidad
        round_quality = sum(round.quality_score for round in session.rounds) / len(session.rounds)
        mode_diversity = len(set(session.thinking_modes_used)) / len(ThinkingMode)
        reasoning_diversity = len(set(session.reasoning_types_used)) / len(ReasoningType)
        
        # Combinar factores
        overall_quality = (round_quality * 0.5 + 
                          mode_diversity * 0.3 + 
                          reasoning_diversity * 0.2)
        
        return min(1.0, overall_quality)
    
    def get_session_status(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Obtiene estado de una sesión."""
        if session_id not in self.active_sessions:
            return None
        
        session = self.active_sessions[session_id]
        
        return {
            'session_id': session_id,
            'initial_query': session.initial_query,
            'rounds_completed': len(session.rounds),
            'max_rounds': self.max_rounds,
            'current_confidence': session.overall_confidence,
            'current_quality': session.overall_quality,
            'thinking_modes_used': [mode.value for mode in session.thinking_modes_used],
            'reasoning_types_used': [type.value for type in session.reasoning_types_used],
            'created_at': session.created_at.isoformat(),
            'is_completed': session.completed_at is not None
        }
    
    def get_multi_round_stats(self) -> Dict[str, Any]:
        """Obtiene estadísticas de pensamiento multi-ronda."""
        return {
            'multi_round_stats': self.multi_round_stats,
            'thinking_engine_stats': self.thinking_engine.thinking_stats,
            'active_sessions': len(self.active_sessions),
            'completed_sessions': len(self.session_history)
        }


if __name__ == "__main__":
    # Test del MultiRoundThinking
    logging.basicConfig(level=logging.INFO)
    
    multi_round = MultiRoundThinking(max_rounds=3)
    
    # Iniciar sesión de pensamiento
    session_id = multi_round.start_thinking_session(
        "How can we improve the performance of our AI system?",
        "We have a system with 20B and 120B models, using T5X for training"
    )
    
    print(f"Sesión iniciada: {session_id}")
    
    # Ejecutar rondas de pensamiento
    for round_num in range(3):
        thinking_round = multi_round.execute_thinking_round(
            session_id,
            thinking_mode=ThinkingMode.ANALYTICAL if round_num == 0 else ThinkingMode.ADAPTIVE,
            reasoning_type=ReasoningType.DEDUCTIVE
        )
        
        if thinking_round:
            print(f"\nRonda {thinking_round.round_number}:")
            print(f"  Confianza: {thinking_round.confidence_score:.2f}")
            print(f"  Calidad: {thinking_round.quality_score:.2f}")
            print(f"  Pasos: {len(thinking_round.steps)}")
            print(f"  Insights: {len(thinking_round.insights)}")
            print(f"  Síntesis: {thinking_round.synthesis[:100]}...")
    
    # Completar sesión
    completed_session = multi_round.complete_thinking_session(session_id)
    
    if completed_session:
        print(f"\nSesión completada:")
        print(f"  Confianza general: {completed_session.overall_confidence:.2f}")
        print(f"  Calidad general: {completed_session.overall_quality:.2f}")
        print(f"  Duración: {completed_session.total_duration_seconds:.2f}s")
        print(f"  Rondas: {len(completed_session.rounds)}")
        print(f"  Conclusión: {completed_session.final_conclusion[:200]}...")
    
    # Mostrar estadísticas
    stats = multi_round.get_multi_round_stats()
    print(f"\nEstadísticas: {stats}")
