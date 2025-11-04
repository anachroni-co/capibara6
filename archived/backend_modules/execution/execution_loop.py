#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Execution Loop - Loop multi-round con corrección automática.
"""

import logging
import time
from typing import Dict, List, Any, Optional, Callable
from datetime import datetime
import json

from .e2b_manager import E2BManager
from .code_detector import CodeDetector, CodeBlock

logger = logging.getLogger(__name__)


class ExecutionAttempt:
    """Representa un intento de ejecución."""
    
    def __init__(self, 
                 attempt_number: int,
                 code: str,
                 language: str,
                 original_code: str = None):
        self.attempt_number = attempt_number
        self.code = code
        self.language = language
        self.original_code = original_code or code
        self.timestamp = datetime.now()
        self.result = None
        self.correction_applied = None
        
    def set_result(self, result: Dict[str, Any]):
        """Establece el resultado de la ejecución."""
        self.result = result
        
    def set_correction(self, correction: str):
        """Establece la corrección aplicada."""
        self.correction_applied = correction
        
    def to_dict(self) -> Dict[str, Any]:
        """Convierte a diccionario."""
        return {
            'attempt_number': self.attempt_number,
            'code': self.code,
            'language': self.language,
            'original_code': self.original_code,
            'timestamp': self.timestamp.isoformat(),
            'result': self.result,
            'correction_applied': self.correction_applied
        }


class ExecutionLoop:
    """Loop de ejecución multi-round con corrección automática."""
    
    def __init__(self, 
                 e2b_manager: E2BManager,
                 model_client: Optional[Callable] = None,
                 max_attempts: int = 3,
                 correction_strategies: Optional[Dict[str, Any]] = None):
        self.e2b_manager = e2b_manager
        self.model_client = model_client
        self.max_attempts = max_attempts
        self.correction_strategies = correction_strategies or {}
        
        self.loop_stats = {
            'total_loops': 0,
            'successful_loops': 0,
            'failed_loops': 0,
            'total_attempts': 0,
            'total_corrections': 0,
            'avg_attempts_per_loop': 0.0,
            'success_rate_by_attempt': {1: 0, 2: 0, 3: 0}
        }
        
        logger.info(f"ExecutionLoop inicializado: max_attempts={max_attempts}")
    
    async def execute_with_correction(self, 
                                    code: str, 
                                    language: str = "python",
                                    context: str = "",
                                    user_intent: str = "") -> Dict[str, Any]:
        """
        Ejecuta código con hasta max_attempts intentos de corrección.
        
        Args:
            code: Código a ejecutar
            language: Lenguaje de programación
            context: Contexto adicional
            user_intent: Intención del usuario
            
        Returns:
            Dict con resultado del loop de ejecución
        """
        start_time = time.time()
        logger.debug(f"Iniciando loop de ejecución: {language}, {len(code)} caracteres")
        
        attempts = []
        final_result = None
        
        try:
            current_code = code
            
            for attempt_num in range(1, self.max_attempts + 1):
                # Crear intento
                attempt = ExecutionAttempt(
                    attempt_number=attempt_num,
                    code=current_code,
                    language=language,
                    original_code=code
                )
                
                # Ejecutar código
                result = await self.e2b_manager.execute_code(
                    code=current_code,
                    language=language
                )
                
                attempt.set_result(result)
                attempts.append(attempt)
                
                logger.info(f"Intento {attempt_num}: success={result['success']}, "
                           f"error={result.get('error_type', 'None')}")
                
                # Si es exitoso, terminar
                if result['success']:
                    final_result = result
                    break
                
                # Si no es el último intento, intentar corrección
                if attempt_num < self.max_attempts:
                    correction = await self._generate_correction(
                        code=current_code,
                        language=language,
                        error=result['error'],
                        error_type=result.get('error_type'),
                        context=context,
                        user_intent=user_intent,
                        previous_attempts=attempts
                    )
                    
                    if correction:
                        attempt.set_correction(correction)
                        current_code = correction
                        logger.info(f"Corrección aplicada en intento {attempt_num}")
                    else:
                        logger.warning(f"No se pudo generar corrección para intento {attempt_num}")
            
            # Si llegamos aquí sin éxito, usar el último resultado
            if not final_result:
                final_result = attempts[-1].result
            
            # Actualizar estadísticas
            self._update_loop_stats(attempts, final_result['success'])
            
            loop_time = time.time() - start_time
            
            return {
                'success': final_result['success'],
                'final_result': final_result,
                'attempts': [attempt.to_dict() for attempt in attempts],
                'total_attempts': len(attempts),
                'corrections_applied': len([a for a in attempts if a.correction_applied]),
                'loop_time': loop_time,
                'language': language,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error en execution loop: {e}")
            return {
                'success': False,
                'error': str(e),
                'attempts': [attempt.to_dict() for attempt in attempts],
                'total_attempts': len(attempts),
                'loop_time': time.time() - start_time,
                'language': language,
                'timestamp': datetime.now().isoformat()
            }
    
    async def _generate_correction(self, 
                                 code: str,
                                 language: str,
                                 error: str,
                                 error_type: str,
                                 context: str,
                                 user_intent: str,
                                 previous_attempts: List[ExecutionAttempt]) -> Optional[str]:
        """Genera corrección para el código."""
        try:
            if self.model_client:
                # Usar modelo real para corrección
                correction_prompt = self._build_correction_prompt(
                    code, language, error, error_type, context, user_intent, previous_attempts
                )
                correction = await self._call_model(correction_prompt)
                return self._extract_code_from_response(correction, language)
            else:
                # Usar estrategias de corrección predefinidas
                return self._apply_correction_strategy(
                    code, language, error, error_type, previous_attempts
                )
                
        except Exception as e:
            logger.error(f"Error generando corrección: {e}")
            return None
    
    def _build_correction_prompt(self, 
                               code: str,
                               language: str,
                               error: str,
                               error_type: str,
                               context: str,
                               user_intent: str,
                               previous_attempts: List[ExecutionAttempt]) -> str:
        """Construye prompt para corrección de código."""
        
        # Información de intentos anteriores
        previous_info = ""
        for attempt in previous_attempts:
            if attempt.result and not attempt.result['success']:
                previous_info += f"Intento {attempt.attempt_number}: {attempt.result['error']}\n"
        
        prompt = f"""
Eres un experto en {language}. El siguiente código tiene un error y necesitas corregirlo.

**Código original:**
```{language}
{code}
```

**Error encontrado:**
Tipo: {error_type}
Mensaje: {error}

**Contexto:**
{context}

**Intención del usuario:**
{user_intent}

**Intentos anteriores:**
{previous_info}

**Instrucciones:**
1. Analiza el error y identifica la causa
2. Corrige el código manteniendo la funcionalidad original
3. Asegúrate de que el código corregido sea sintácticamente correcto
4. Responde SOLO con el código corregido, sin explicaciones adicionales

**Código corregido:**
```{language}
"""
        
        return prompt
    
    async def _call_model(self, prompt: str) -> str:
        """Llama al modelo para corrección."""
        # Implementación mock - en producción usaría el cliente real
        logger.debug("Llamada mock al modelo para corrección")
        
        # Simular diferentes tipos de corrección basado en el prompt
        if "SyntaxError" in prompt:
            return "print('Hello, World!')"  # Corrección simple
        elif "NameError" in prompt:
            return "x = 5\nprint(x)"  # Definir variable
        elif "TypeError" in prompt:
            return "result = str(5) + 'hello'"  # Conversión de tipos
        
        return "print('Corrected code')"
    
    def _extract_code_from_response(self, response: str, language: str) -> str:
        """Extrae código de la respuesta del modelo."""
        # Buscar bloques de código en la respuesta
        import re
        
        # Patrón para bloques de código
        pattern = rf'```{language}\s*\n(.*?)\n```'
        match = re.search(pattern, response, re.DOTALL)
        
        if match:
            return match.group(1).strip()
        
        # Si no hay bloques, buscar código entre backticks
        pattern = r'```\s*\n(.*?)\n```'
        match = re.search(pattern, response, re.DOTALL)
        
        if match:
            return match.group(1).strip()
        
        # Si no hay backticks, asumir que toda la respuesta es código
        return response.strip()
    
    def _apply_correction_strategy(self, 
                                 code: str,
                                 language: str,
                                 error: str,
                                 error_type: str,
                                 previous_attempts: List[ExecutionAttempt]) -> Optional[str]:
        """Aplica estrategias de corrección predefinidas."""
        
        # Estrategias básicas por tipo de error
        strategies = {
            'SyntaxError': self._fix_syntax_error,
            'NameError': self._fix_name_error,
            'TypeError': self._fix_type_error,
            'IndentationError': self._fix_indentation_error,
            'ImportError': self._fix_import_error,
            'AttributeError': self._fix_attribute_error
        }
        
        strategy = strategies.get(error_type)
        if strategy:
            return strategy(code, language, error)
        
        # Estrategia genérica
        return self._fix_generic_error(code, language, error)
    
    def _fix_syntax_error(self, code: str, language: str, error: str) -> Optional[str]:
        """Corrige errores de sintaxis."""
        if language == 'python':
            # Corregir paréntesis faltantes
            if "unexpected EOF" in error or "unterminated" in error:
                if code.count('(') > code.count(')'):
                    return code + ')'
                elif code.count('[') > code.count(']'):
                    return code + ']'
                elif code.count('{') > code.count('}'):
                    return code + '}'
            
            # Corregir comillas
            if "EOL while scanning string literal" in error:
                lines = code.split('\n')
                for i, line in enumerate(lines):
                    if line.count('"') % 2 == 1:
                        lines[i] = line + '"'
                return '\n'.join(lines)
        
        return None
    
    def _fix_name_error(self, code: str, language: str, error: str) -> Optional[str]:
        """Corrige errores de nombres no definidos."""
        import re
        
        # Extraer nombre de variable del error
        match = re.search(r"name '(\w+)' is not defined", error)
        if match:
            var_name = match.group(1)
            
            if language == 'python':
                # Agregar definición de variable
                if var_name in ['x', 'y', 'z']:
                    return f"{var_name} = 0\n{code}"
                elif var_name in ['name', 'user', 'username']:
                    return f"{var_name} = 'default'\n{code}"
                elif var_name in ['data', 'result', 'output']:
                    return f"{var_name} = []\n{code}"
        
        return None
    
    def _fix_type_error(self, code: str, language: str, error: str) -> Optional[str]:
        """Corrige errores de tipo."""
        if "can only concatenate str" in error:
            # Agregar conversión a string
            lines = code.split('\n')
            for i, line in enumerate(lines):
                if '+' in line and 'str(' not in line:
                    # Buscar operación de concatenación
                    parts = line.split('+')
                    if len(parts) == 2:
                        left = parts[0].strip()
                        right = parts[1].strip()
                        lines[i] = f"str({left}) + str({right})"
            return '\n'.join(lines)
        
        return None
    
    def _fix_indentation_error(self, code: str, language: str, error: str) -> Optional[str]:
        """Corrige errores de indentación."""
        if language == 'python':
            # Normalizar indentación a 4 espacios
            lines = code.split('\n')
            corrected_lines = []
            
            for line in lines:
                if line.strip():  # Si la línea no está vacía
                    # Contar espacios/tabs al inicio
                    indent = len(line) - len(line.lstrip())
                    # Convertir a múltiplos de 4
                    new_indent = (indent // 4) * 4
                    corrected_lines.append(' ' * new_indent + line.lstrip())
                else:
                    corrected_lines.append(line)
            
            return '\n'.join(corrected_lines)
        
        return None
    
    def _fix_import_error(self, code: str, language: str, error: str) -> Optional[str]:
        """Corrige errores de importación."""
        # Para errores de importación, intentar usar alternativas
        if "No module named" in error:
            # Mapeo de módulos alternativos
            alternatives = {
                'numpy': 'import math',
                'pandas': 'import csv',
                'requests': 'import urllib.request',
                'matplotlib': 'print("Plot functionality not available")'
            }
            
            for module, alternative in alternatives.items():
                if module in error:
                    return code.replace(f'import {module}', alternative)
        
        return None
    
    def _fix_attribute_error(self, code: str, language: str, error: str) -> Optional[str]:
        """Corrige errores de atributos."""
        # Estrategias básicas para errores de atributos
        if "'NoneType' object has no attribute" in error:
            # Agregar verificación de None
            lines = code.split('\n')
            for i, line in enumerate(lines):
                if '.' in line and 'if' not in line:
                    # Agregar verificación
                    var = line.split('.')[0].strip()
                    lines[i] = f"if {var} is not None:\n    {line}"
            return '\n'.join(lines)
        
        return None
    
    def _fix_generic_error(self, code: str, language: str, error: str) -> Optional[str]:
        """Corrección genérica para errores no específicos."""
        # Estrategias genéricas
        if language == 'python':
            # Agregar try-except
            return f"try:\n    {code}\nexcept Exception as e:\n    print(f'Error: {{e}}')"
        
        return None
    
    def _update_loop_stats(self, attempts: List[ExecutionAttempt], success: bool):
        """Actualiza estadísticas del loop."""
        self.loop_stats['total_loops'] += 1
        
        if success:
            self.loop_stats['successful_loops'] += 1
        else:
            self.loop_stats['failed_loops'] += 1
        
        self.loop_stats['total_attempts'] += len(attempts)
        self.loop_stats['total_corrections'] += len([a for a in attempts if a.correction_applied])
        
        # Actualizar promedio de intentos
        current_avg = self.loop_stats['avg_attempts_per_loop']
        total_loops = self.loop_stats['total_loops']
        new_attempts = len(attempts)
        
        self.loop_stats['avg_attempts_per_loop'] = (
            (current_avg * (total_loops - 1) + new_attempts) / total_loops
        )
        
        # Estadísticas por intento
        if success:
            success_attempt = len(attempts)
            if success_attempt in self.loop_stats['success_rate_by_attempt']:
                self.loop_stats['success_rate_by_attempt'][success_attempt] += 1
    
    def get_stats(self) -> Dict[str, Any]:
        """Retorna estadísticas del loop."""
        success_rate = 0.0
        if self.loop_stats['total_loops'] > 0:
            success_rate = self.loop_stats['successful_loops'] / self.loop_stats['total_loops']
        
        return {
            'loop_stats': self.loop_stats,
            'success_rate': success_rate,
            'config': {
                'max_attempts': self.max_attempts,
                'correction_strategies_available': len(self.correction_strategies)
            }
        }


if __name__ == "__main__":
    # Test del ExecutionLoop
    import asyncio
    logging.basicConfig(level=logging.INFO)
    
    async def test_execution_loop():
        e2b_manager = E2BManager()
        execution_loop = ExecutionLoop(e2b_manager)
        
        # Test con código que tiene error
        result = await execution_loop.execute_with_correction(
            code="print('Hello, World!'",  # Syntax error - falta paréntesis
            language="python",
            context="Simple greeting function",
            user_intent="Print a greeting message"
        )
        
        print(f"Loop result:")
        print(f"Success: {result['success']}")
        print(f"Total attempts: {result['total_attempts']}")
        print(f"Corrections applied: {result['corrections_applied']}")
        print(f"Loop time: {result['loop_time']:.2f}s")
        
        # Mostrar intentos
        for i, attempt in enumerate(result['attempts']):
            print(f"\nAttempt {i+1}:")
            print(f"  Code: {attempt['code'][:50]}...")
            print(f"  Success: {attempt['result']['success']}")
            if attempt['correction_applied']:
                print(f"  Correction: {attempt['correction_applied'][:50]}...")
        
        # Mostrar estadísticas
        stats = execution_loop.get_stats()
        print(f"\nStats: {json.dumps(stats, indent=2)}")
        
        # Limpiar
        await e2b_manager.cleanup()
    
    asyncio.run(test_execution_loop())
