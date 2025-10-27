#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ACE Reflector - Analiza respuestas post-generación para mejorar playbooks.
"""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import json

logger = logging.getLogger(__name__)


class ReflectionPrompts:
    """Prompts para auto-reflexión del sistema."""
    
    @staticmethod
    def build_reflection_prompt(query: str, response: str, context: str = "") -> str:
        """Construye el prompt para reflexión."""
        return f"""
Analiza la siguiente interacción y evalúa la calidad de la respuesta:

**Query del usuario:**
{query}

**Contexto utilizado:**
{context[:500] if context else "Ninguno"}

**Respuesta generada:**
{response}

**Evalúa la respuesta en los siguientes aspectos:**

1. **Precisión y completitud (0-10):** ¿La respuesta es precisa y completa?
2. **Relevancia (0-10):** ¿La respuesta es relevante para la query?
3. **Claridad (0-10):** ¿La respuesta es clara y bien estructurada?
4. **Utilidad (0-10):** ¿La respuesta es útil para el usuario?
5. **Errores factuales (0-10):** ¿Hay errores factuales o alucinaciones? (10 = sin errores)

**Preguntas específicas:**
- ¿Hubo alucinaciones o errores factuales?
- ¿El tono y formato fueron apropiados?
- ¿Qué podría mejorarse?
- ¿La respuesta demuestra comprensión del contexto?

**Formato de respuesta (JSON):**
{{
    "scores": {{
        "accuracy": <0-10>,
        "relevance": <0-10>,
        "clarity": <0-10>,
        "utility": <0-10>,
        "factual_correctness": <0-10>
    }},
    "overall_score": <0-10>,
    "has_hallucinations": <true/false>,
    "has_factual_errors": <true/false>,
    "tone_appropriate": <true/false>,
    "improvements": ["<sugerencia1>", "<sugerencia2>"],
    "insights": "<análisis general>",
    "should_add_to_playbook": <true/false>
}}
"""

    @staticmethod
    def build_domain_analysis_prompt(query: str, response: str, domain: str) -> str:
        """Construye prompt para análisis de dominio específico."""
        return f"""
Analiza esta interacción en el contexto del dominio '{domain}':

**Query:** {query}
**Respuesta:** {response}

**Evalúa:**
1. ¿La respuesta demuestra conocimiento del dominio {domain}?
2. ¿Se utilizaron conceptos y terminología apropiados?
3. ¿La respuesta es técnicamente correcta para este dominio?
4. ¿Se proporcionaron ejemplos relevantes?

**Formato de respuesta (JSON):**
{{
    "domain_expertise": <0-10>,
    "technical_accuracy": <0-10>,
    "terminology_appropriate": <true/false>,
    "examples_relevant": <true/false>,
    "domain_insights": "<análisis específico del dominio>"
}}
"""

    @staticmethod
    def build_pattern_extraction_prompt(query: str, response: str, context: str) -> str:
        """Construye prompt para extraer patrones."""
        return f"""
Extrae patrones útiles de esta interacción exitosa:

**Query:** {query}
**Contexto:** {context[:300]}
**Respuesta:** {response}

**Identifica:**
1. Patrón de query que podría reutilizarse
2. Template de contexto que funcionó bien
3. Estructura de respuesta efectiva

**Formato de respuesta (JSON):**
{{
    "query_pattern": "<patrón de query reutilizable>",
    "context_template": "<template de contexto efectivo>",
    "response_structure": "<estructura de respuesta que funcionó>",
    "key_elements": ["<elemento1>", "<elemento2>"],
    "confidence": <0-10>
}}
"""


class ACEReflector:
    """Analiza respuestas post-generación para mejorar playbooks."""
    
    def __init__(self, 
                 model_client=None,  # Cliente del modelo LLM
                 reflection_threshold: float = 0.7,
                 sampling_rate: float = 0.1):  # 10% sampling
        self.model_client = model_client
        self.reflection_threshold = reflection_threshold
        self.sampling_rate = sampling_rate
        self.prompts = ReflectionPrompts()
        
        self.reflection_stats = {
            'total_reflections': 0,
            'successful_reflections': 0,
            'patterns_extracted': 0,
            'avg_quality_score': 0.0,
            'hallucination_rate': 0.0
        }
        
        logger.info(f"ACEReflector inicializado con threshold={reflection_threshold}, sampling={sampling_rate}")
    
    def reflect(self, 
                query: str, 
                response: str, 
                context: str = "",
                domain: str = "general",
                user_feedback: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Realiza auto-reflexión sobre la respuesta generada.
        
        Args:
            query: Query original del usuario
            response: Respuesta generada
            context: Contexto utilizado
            domain: Dominio de la interacción
            user_feedback: Feedback del usuario (opcional)
            
        Returns:
            Dict con análisis de reflexión
        """
        start_time = datetime.now()
        logger.debug(f"Reflexionando sobre respuesta para query: '{query[:100]}...'")
        
        try:
            # 1. Decidir si hacer reflexión (sampling)
            if not self._should_reflect():
                return self._create_skipped_reflection()
            
            # 2. Realizar reflexión principal
            main_reflection = self._perform_main_reflection(query, response, context)
            
            # 3. Análisis de dominio específico
            domain_analysis = self._perform_domain_analysis(query, response, domain)
            
            # 4. Extracción de patrones si la respuesta es de alta calidad
            pattern_extraction = None
            if main_reflection.get('overall_score', 0) >= self.reflection_threshold:
                pattern_extraction = self._extract_patterns(query, response, context)
            
            # 5. Combinar análisis
            combined_analysis = self._combine_analyses(
                main_reflection, domain_analysis, pattern_extraction, user_feedback
            )
            
            # 6. Actualizar estadísticas
            self._update_reflection_stats(combined_analysis)
            
            reflection_time = (datetime.now() - start_time).total_seconds() * 1000
            combined_analysis['reflection_time_ms'] = reflection_time
            
            logger.info(f"Reflexión completada: score={combined_analysis.get('overall_score', 0):.1f}, "
                       f"hallucinations={combined_analysis.get('has_hallucinations', False)}, "
                       f"{reflection_time:.1f}ms")
            
            return combined_analysis
            
        except Exception as e:
            logger.error(f"Error en reflexión: {e}")
            return {
                'success': False,
                'error': str(e),
                'reflection_time_ms': (datetime.now() - start_time).total_seconds() * 1000
            }
    
    def _should_reflect(self) -> bool:
        """Decide si realizar reflexión basado en sampling rate."""
        import random
        return random.random() < self.sampling_rate
    
    def _create_skipped_reflection(self) -> Dict[str, Any]:
        """Crea resultado para reflexión omitida."""
        return {
            'success': True,
            'skipped': True,
            'reason': 'sampling_rate',
            'overall_score': 0.0,
            'should_add_to_playbook': False
        }
    
    def _perform_main_reflection(self, query: str, response: str, context: str) -> Dict[str, Any]:
        """Realiza reflexión principal."""
        if self.model_client:
            # Usar modelo real
            prompt = self.prompts.build_reflection_prompt(query, response, context)
            analysis = self._call_model(prompt)
            return self._parse_reflection_response(analysis)
        else:
            # Mock para testing
            return self._mock_reflection(query, response)
    
    def _perform_domain_analysis(self, query: str, response: str, domain: str) -> Dict[str, Any]:
        """Realiza análisis específico del dominio."""
        if self.model_client:
            prompt = self.prompts.build_domain_analysis_prompt(query, response, domain)
            analysis = self._call_model(prompt)
            return self._parse_domain_response(analysis)
        else:
            # Mock para testing
            return self._mock_domain_analysis(domain)
    
    def _extract_patterns(self, query: str, response: str, context: str) -> Dict[str, Any]:
        """Extrae patrones de la interacción exitosa."""
        if self.model_client:
            prompt = self.prompts.build_pattern_extraction_prompt(query, response, context)
            analysis = self._call_model(prompt)
            return self._parse_pattern_response(analysis)
        else:
            # Mock para testing
            return self._mock_pattern_extraction(query)
    
    def _call_model(self, prompt: str) -> str:
        """Llama al modelo LLM."""
        # Implementación mock - en producción usaría el cliente real
        logger.debug("Llamada mock al modelo LLM")
        return '{"overall_score": 8.5, "has_hallucinations": false}'
    
    def _parse_reflection_response(self, response: str) -> Dict[str, Any]:
        """Parsea la respuesta de reflexión del modelo."""
        try:
            # Intentar parsear JSON
            if response.strip().startswith('{'):
                return json.loads(response)
            else:
                # Si no es JSON válido, crear respuesta mock
                return self._mock_reflection("", "")
        except json.JSONDecodeError:
            logger.warning("Error parseando respuesta de reflexión, usando mock")
            return self._mock_reflection("", "")
    
    def _parse_domain_response(self, response: str) -> Dict[str, Any]:
        """Parsea la respuesta de análisis de dominio."""
        try:
            if response.strip().startswith('{'):
                return json.loads(response)
            else:
                return self._mock_domain_analysis("general")
        except json.JSONDecodeError:
            return self._mock_domain_analysis("general")
    
    def _parse_pattern_response(self, response: str) -> Dict[str, Any]:
        """Parsea la respuesta de extracción de patrones."""
        try:
            if response.strip().startswith('{'):
                return json.loads(response)
            else:
                return self._mock_pattern_extraction("")
        except json.JSONDecodeError:
            return self._mock_pattern_extraction("")
    
    def _mock_reflection(self, query: str, response: str) -> Dict[str, Any]:
        """Mock de reflexión para testing."""
        # Simular análisis basado en longitud y contenido
        response_length = len(response)
        has_code = '```' in response or 'def ' in response or 'function' in response
        has_examples = 'example' in response.lower() or 'for example' in response.lower()
        
        # Calcular score basado en heurísticas simples
        base_score = 6.0
        if response_length > 100:
            base_score += 1.0
        if has_code:
            base_score += 1.0
        if has_examples:
            base_score += 0.5
        if response_length > 500:
            base_score += 1.0
        
        overall_score = min(10.0, base_score)
        
        return {
            'scores': {
                'accuracy': overall_score - 0.5,
                'relevance': overall_score,
                'clarity': overall_score - 0.3,
                'utility': overall_score - 0.2,
                'factual_correctness': overall_score - 0.1
            },
            'overall_score': overall_score,
            'has_hallucinations': False,
            'has_factual_errors': False,
            'tone_appropriate': True,
            'improvements': ['Could be more detailed', 'Add more examples'],
            'insights': f'Response of {response_length} characters with good structure',
            'should_add_to_playbook': overall_score >= self.reflection_threshold
        }
    
    def _mock_domain_analysis(self, domain: str) -> Dict[str, Any]:
        """Mock de análisis de dominio."""
        return {
            'domain_expertise': 8.0,
            'technical_accuracy': 7.5,
            'terminology_appropriate': True,
            'examples_relevant': True,
            'domain_insights': f'Good understanding of {domain} concepts'
        }
    
    def _mock_pattern_extraction(self, query: str) -> Dict[str, Any]:
        """Mock de extracción de patrones."""
        return {
            'query_pattern': query[:50] + "..." if len(query) > 50 else query,
            'context_template': f"Context for {query.split()[0] if query else 'query'}",
            'response_structure': "Introduction -> Explanation -> Examples -> Summary",
            'key_elements': ['definition', 'examples', 'best_practices'],
            'confidence': 7.5
        }
    
    def _combine_analyses(self, 
                         main_reflection: Dict[str, Any],
                         domain_analysis: Dict[str, Any],
                         pattern_extraction: Optional[Dict[str, Any]],
                         user_feedback: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Combina todos los análisis en un resultado final."""
        combined = {
            'success': True,
            'timestamp': datetime.now().isoformat(),
            'main_analysis': main_reflection,
            'domain_analysis': domain_analysis,
            'pattern_extraction': pattern_extraction,
            'user_feedback': user_feedback
        }
        
        # Calcular score final
        main_score = main_reflection.get('overall_score', 0)
        domain_score = domain_analysis.get('domain_expertise', 0)
        
        # Ponderar scores
        final_score = (main_score * 0.7) + (domain_score * 0.3)
        combined['final_score'] = final_score
        
        # Decidir si agregar al playbook
        combined['should_add_to_playbook'] = (
            final_score >= self.reflection_threshold and
            not main_reflection.get('has_hallucinations', False) and
            not main_reflection.get('has_factual_errors', False)
        )
        
        # Agregar recomendaciones
        combined['recommendations'] = self._generate_recommendations(
            main_reflection, domain_analysis, user_feedback
        )
        
        return combined
    
    def _generate_recommendations(self, 
                                main_reflection: Dict[str, Any],
                                domain_analysis: Dict[str, Any],
                                user_feedback: Optional[Dict[str, Any]]) -> List[str]:
        """Genera recomendaciones basadas en el análisis."""
        recommendations = []
        
        # Recomendaciones basadas en scores bajos
        scores = main_reflection.get('scores', {})
        if scores.get('accuracy', 10) < 7:
            recommendations.append("Improve factual accuracy")
        if scores.get('clarity', 10) < 7:
            recommendations.append("Enhance response clarity")
        if scores.get('utility', 10) < 7:
            recommendations.append("Make response more actionable")
        
        # Recomendaciones de dominio
        if domain_analysis.get('technical_accuracy', 10) < 7:
            recommendations.append("Improve technical accuracy for domain")
        if not domain_analysis.get('terminology_appropriate', True):
            recommendations.append("Use more appropriate domain terminology")
        
        # Recomendaciones de usuario
        if user_feedback:
            if user_feedback.get('rating', 5) < 3:
                recommendations.append("Address user feedback concerns")
        
        return recommendations
    
    def _update_reflection_stats(self, analysis: Dict[str, Any]):
        """Actualiza estadísticas de reflexión."""
        self.reflection_stats['total_reflections'] += 1
        
        if analysis.get('success', False):
            self.reflection_stats['successful_reflections'] += 1
            
            # Actualizar score promedio
            current_avg = self.reflection_stats['avg_quality_score']
            total_refs = self.reflection_stats['total_reflections']
            new_score = analysis.get('final_score', 0)
            
            self.reflection_stats['avg_quality_score'] = (
                (current_avg * (total_refs - 1) + new_score) / total_refs
            )
            
            # Actualizar tasa de alucinaciones
            has_hallucinations = analysis.get('main_analysis', {}).get('has_hallucinations', False)
            if has_hallucinations:
                hallucination_count = self.reflection_stats.get('hallucination_count', 0) + 1
                self.reflection_stats['hallucination_count'] = hallucination_count
                self.reflection_stats['hallucination_rate'] = hallucination_count / total_refs
            
            # Contar patrones extraídos
            if analysis.get('pattern_extraction'):
                self.reflection_stats['patterns_extracted'] += 1
    
    def get_stats(self) -> Dict[str, Any]:
        """Retorna estadísticas del reflector."""
        return {
            'reflection_stats': self.reflection_stats,
            'config': {
                'reflection_threshold': self.reflection_threshold,
                'sampling_rate': self.sampling_rate
            }
        }
    
    def set_sampling_rate(self, rate: float):
        """Ajusta la tasa de sampling."""
        self.sampling_rate = max(0.0, min(1.0, rate))
        logger.info(f"Tasa de sampling ajustada a {self.sampling_rate}")


if __name__ == "__main__":
    # Test del ACEReflector
    logging.basicConfig(level=logging.INFO)
    
    reflector = ACEReflector()
    
    # Test de reflexión
    test_query = "How to create a Python function?"
    test_response = """
To create a Python function, use the 'def' keyword followed by the function name and parameters:

```python
def greet(name):
    return f"Hello, {name}!"

# Usage
message = greet("World")
print(message)  # Output: Hello, World!
```

Key points:
- Use 'def' keyword
- Function name should be descriptive
- Parameters go in parentheses
- Use 'return' to send back a value
"""
    
    result = reflector.reflect(test_query, test_response, domain="python")
    
    print(f"Reflection result:")
    print(f"Success: {result.get('success', False)}")
    print(f"Final score: {result.get('final_score', 0):.1f}")
    print(f"Should add to playbook: {result.get('should_add_to_playbook', False)}")
    print(f"Recommendations: {result.get('recommendations', [])}")
    
    # Mostrar estadísticas
    stats = reflector.get_stats()
    print(f"\nStats: {json.dumps(stats, indent=2)}")
