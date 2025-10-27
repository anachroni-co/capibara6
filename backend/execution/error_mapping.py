#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Error Mapping - Mapeo de errores comunes y estrategias de corrección.
"""

import logging
import re
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from enum import Enum

logger = logging.getLogger(__name__)


class ErrorSeverity(Enum):
    """Severidad de errores."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ErrorCategory(Enum):
    """Categorías de errores."""
    SYNTAX = "syntax"
    RUNTIME = "runtime"
    LOGIC = "logic"
    IMPORT = "import"
    TYPE = "type"
    RESOURCE = "resource"
    SECURITY = "security"


class ErrorPattern:
    """Patrón de error con estrategias de corrección."""
    
    def __init__(self, 
                 error_type: str,
                 category: ErrorCategory,
                 severity: ErrorSeverity,
                 patterns: List[str],
                 correction_strategies: List[Dict[str, Any]],
                 context_requirements: List[str] = None):
        self.error_type = error_type
        self.category = category
        self.severity = severity
        self.patterns = patterns
        self.correction_strategies = correction_strategies
        self.context_requirements = context_requirements or []
        
        # Estadísticas
        self.occurrence_count = 0
        self.successful_corrections = 0
        self.last_seen = None
        
    def matches(self, error_message: str) -> bool:
        """Verifica si el error coincide con este patrón."""
        error_lower = error_message.lower()
        for pattern in self.patterns:
            if re.search(pattern, error_lower, re.IGNORECASE):
                return True
        return False
    
    def get_correction_strategy(self, 
                              error_message: str, 
                              code: str, 
                              language: str,
                              context: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
        """Obtiene la mejor estrategia de corrección para el error."""
        # Actualizar estadísticas
        self.occurrence_count += 1
        self.last_seen = datetime.now()
        
        # Seleccionar estrategia basada en el contexto
        for strategy in self.correction_strategies:
            if self._strategy_applies(strategy, error_message, code, language, context):
                return strategy
        
        # Retornar estrategia por defecto
        return self.correction_strategies[0] if self.correction_strategies else None
    
    def _strategy_applies(self, 
                        strategy: Dict[str, Any],
                        error_message: str,
                        code: str,
                        language: str,
                        context: Dict[str, Any]) -> bool:
        """Verifica si una estrategia se aplica al contexto actual."""
        conditions = strategy.get('conditions', {})
        
        # Verificar lenguaje
        if 'languages' in conditions:
            if language not in conditions['languages']:
                return False
        
        # Verificar patrones en el código
        if 'code_patterns' in conditions:
            for pattern in conditions['code_patterns']:
                if not re.search(pattern, code, re.IGNORECASE):
                    return False
        
        # Verificar contexto
        if 'context_requirements' in conditions:
            if not context:
                return False
            for req in conditions['context_requirements']:
                if req not in context:
                    return False
        
        return True
    
    def record_correction_success(self, success: bool):
        """Registra el éxito de una corrección."""
        if success:
            self.successful_corrections += 1
    
    def get_success_rate(self) -> float:
        """Calcula la tasa de éxito de corrección."""
        if self.occurrence_count == 0:
            return 0.0
        return self.successful_corrections / self.occurrence_count


class ErrorMapper:
    """Mapea errores a estrategias de corrección."""
    
    def __init__(self):
        self.error_patterns = self._initialize_error_patterns()
        self.mapping_stats = {
            'total_errors_mapped': 0,
            'successful_corrections': 0,
            'failed_corrections': 0,
            'errors_by_category': {},
            'errors_by_severity': {}
        }
        
        logger.info("ErrorMapper inicializado")
    
    def _initialize_error_patterns(self) -> List[ErrorPattern]:
        """Inicializa patrones de error comunes."""
        patterns = []
        
        # Errores de sintaxis
        patterns.append(ErrorPattern(
            error_type="SyntaxError",
            category=ErrorCategory.SYNTAX,
            severity=ErrorSeverity.HIGH,
            patterns=[
                r"syntax error",
                r"invalid syntax",
                r"unexpected eof",
                r"unterminated",
                r"missing.*parenthesis",
                r"missing.*bracket"
            ],
            correction_strategies=[
                {
                    'name': 'fix_parentheses',
                    'description': 'Corregir paréntesis faltantes',
                    'conditions': {'languages': ['python', 'javascript']},
                    'correction_function': 'fix_missing_parentheses',
                    'confidence': 0.8
                },
                {
                    'name': 'fix_quotes',
                    'description': 'Corregir comillas no cerradas',
                    'conditions': {'languages': ['python', 'javascript']},
                    'correction_function': 'fix_unclosed_quotes',
                    'confidence': 0.9
                }
            ]
        ))
        
        # Errores de nombres no definidos
        patterns.append(ErrorPattern(
            error_type="NameError",
            category=ErrorCategory.RUNTIME,
            severity=ErrorSeverity.MEDIUM,
            patterns=[
                r"name.*is not defined",
                r"undefined variable",
                r"undefined name"
            ],
            correction_strategies=[
                {
                    'name': 'define_variable',
                    'description': 'Definir variable faltante',
                    'conditions': {'languages': ['python', 'javascript']},
                    'correction_function': 'define_missing_variable',
                    'confidence': 0.7
                },
                {
                    'name': 'fix_typo',
                    'description': 'Corregir error tipográfico en nombre',
                    'conditions': {'languages': ['python', 'javascript']},
                    'correction_function': 'fix_variable_typo',
                    'confidence': 0.6
                }
            ]
        ))
        
        # Errores de tipo
        patterns.append(ErrorPattern(
            error_type="TypeError",
            category=ErrorCategory.TYPE,
            severity=ErrorSeverity.MEDIUM,
            patterns=[
                r"can only concatenate str",
                r"unsupported operand type",
                r"object of type.*has no len",
                r"argument must be.*not.*"
            ],
            correction_strategies=[
                {
                    'name': 'type_conversion',
                    'description': 'Convertir tipos para operaciones',
                    'conditions': {'languages': ['python', 'javascript']},
                    'correction_function': 'add_type_conversion',
                    'confidence': 0.8
                },
                {
                    'name': 'fix_operator',
                    'description': 'Corregir operador inapropiado',
                    'conditions': {'languages': ['python', 'javascript']},
                    'correction_function': 'fix_operator_usage',
                    'confidence': 0.7
                }
            ]
        ))
        
        # Errores de indentación
        patterns.append(ErrorPattern(
            error_type="IndentationError",
            category=ErrorCategory.SYNTAX,
            severity=ErrorSeverity.HIGH,
            patterns=[
                r"indentation error",
                r"unindent does not match",
                r"expected an indented block"
            ],
            correction_strategies=[
                {
                    'name': 'fix_indentation',
                    'description': 'Corregir indentación',
                    'conditions': {'languages': ['python']},
                    'correction_function': 'normalize_indentation',
                    'confidence': 0.9
                }
            ]
        ))
        
        # Errores de importación
        patterns.append(ErrorPattern(
            error_type="ImportError",
            category=ErrorCategory.IMPORT,
            severity=ErrorSeverity.MEDIUM,
            patterns=[
                r"no module named",
                r"cannot import name",
                r"module not found"
            ],
            correction_strategies=[
                {
                    'name': 'alternative_import',
                    'description': 'Usar importación alternativa',
                    'conditions': {'languages': ['python']},
                    'correction_function': 'use_alternative_import',
                    'confidence': 0.6
                },
                {
                    'name': 'remove_import',
                    'description': 'Remover importación problemática',
                    'conditions': {'languages': ['python']},
                    'correction_function': 'remove_problematic_import',
                    'confidence': 0.5
                }
            ]
        ))
        
        # Errores de atributos
        patterns.append(ErrorPattern(
            error_type="AttributeError",
            category=ErrorCategory.RUNTIME,
            severity=ErrorSeverity.MEDIUM,
            patterns=[
                r"object has no attribute",
                r"nonetype.*has no attribute",
                r"attribute.*does not exist"
            ],
            correction_strategies=[
                {
                    'name': 'null_check',
                    'description': 'Agregar verificación de None',
                    'conditions': {'languages': ['python']},
                    'correction_function': 'add_null_check',
                    'confidence': 0.7
                },
                {
                    'name': 'fix_attribute',
                    'description': 'Corregir nombre de atributo',
                    'conditions': {'languages': ['python', 'javascript']},
                    'correction_function': 'fix_attribute_name',
                    'confidence': 0.6
                }
            ]
        ))
        
        # Errores de índice
        patterns.append(ErrorPattern(
            error_type="IndexError",
            category=ErrorCategory.RUNTIME,
            severity=ErrorSeverity.MEDIUM,
            patterns=[
                r"list index out of range",
                r"string index out of range",
                r"index.*out of bounds"
            ],
            correction_strategies=[
                {
                    'name': 'bounds_check',
                    'description': 'Agregar verificación de límites',
                    'conditions': {'languages': ['python', 'javascript']},
                    'correction_function': 'add_bounds_check',
                    'confidence': 0.8
                },
                {
                    'name': 'safe_access',
                    'description': 'Usar acceso seguro a elementos',
                    'conditions': {'languages': ['python']},
                    'correction_function': 'use_safe_access',
                    'confidence': 0.7
                }
            ]
        ))
        
        # Errores de clave
        patterns.append(ErrorPattern(
            error_type="KeyError",
            category=ErrorCategory.RUNTIME,
            severity=ErrorSeverity.MEDIUM,
            patterns=[
                r"keyerror",
                r"key.*not found",
                r"dictionary.*has no key"
            ],
            correction_strategies=[
                {
                    'name': 'key_check',
                    'description': 'Verificar existencia de clave',
                    'conditions': {'languages': ['python']},
                    'correction_function': 'add_key_check',
                    'confidence': 0.8
                },
                {
                    'name': 'default_value',
                    'description': 'Usar valor por defecto',
                    'conditions': {'languages': ['python']},
                    'correction_function': 'use_default_value',
                    'confidence': 0.7
                }
            ]
        ))
        
        return patterns
    
    def map_error(self, 
                 error_message: str,
                 error_type: str,
                 code: str,
                 language: str,
                 context: Dict[str, Any] = None) -> Optional[ErrorPattern]:
        """Mapea un error a un patrón y estrategia de corrección."""
        logger.debug(f"Mapeando error: {error_type} - {error_message[:100]}...")
        
        # Buscar patrón que coincida
        for pattern in self.error_patterns:
            if pattern.error_type == error_type and pattern.matches(error_message):
                self._update_mapping_stats(pattern)
                return pattern
        
        # Si no se encuentra patrón específico, buscar por mensaje
        for pattern in self.error_patterns:
            if pattern.matches(error_message):
                self._update_mapping_stats(pattern)
                return pattern
        
        logger.warning(f"No se encontró patrón para error: {error_type} - {error_message}")
        return None
    
    def get_correction_strategy(self, 
                              error_message: str,
                              error_type: str,
                              code: str,
                              language: str,
                              context: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
        """Obtiene estrategia de corrección para un error."""
        pattern = self.map_error(error_message, error_type, code, language, context)
        
        if pattern:
            strategy = pattern.get_correction_strategy(error_message, code, language, context)
            if strategy:
                logger.info(f"Estrategia encontrada: {strategy['name']} (confidence: {strategy['confidence']})")
                return strategy
        
        return None
    
    def _update_mapping_stats(self, pattern: ErrorPattern):
        """Actualiza estadísticas de mapeo."""
        self.mapping_stats['total_errors_mapped'] += 1
        
        # Estadísticas por categoría
        category = pattern.category.value
        if category not in self.mapping_stats['errors_by_category']:
            self.mapping_stats['errors_by_category'][category] = 0
        self.mapping_stats['errors_by_category'][category] += 1
        
        # Estadísticas por severidad
        severity = pattern.severity.value
        if severity not in self.mapping_stats['errors_by_severity']:
            self.mapping_stats['errors_by_severity'][severity] = 0
        self.mapping_stats['errors_by_severity'][severity] += 1
    
    def record_correction_result(self, 
                               error_type: str,
                               error_message: str,
                               success: bool):
        """Registra el resultado de una corrección."""
        pattern = self.map_error(error_message, error_type, "", "")
        if pattern:
            pattern.record_correction_success(success)
            
            if success:
                self.mapping_stats['successful_corrections'] += 1
            else:
                self.mapping_stats['failed_corrections'] += 1
    
    def get_error_statistics(self) -> Dict[str, Any]:
        """Retorna estadísticas de errores."""
        total_corrections = (self.mapping_stats['successful_corrections'] + 
                           self.mapping_stats['failed_corrections'])
        
        correction_success_rate = 0.0
        if total_corrections > 0:
            correction_success_rate = (self.mapping_stats['successful_corrections'] / 
                                     total_corrections)
        
        # Estadísticas por patrón
        pattern_stats = {}
        for pattern in self.error_patterns:
            pattern_stats[pattern.error_type] = {
                'occurrence_count': pattern.occurrence_count,
                'successful_corrections': pattern.successful_corrections,
                'success_rate': pattern.get_success_rate(),
                'last_seen': pattern.last_seen.isoformat() if pattern.last_seen else None
            }
        
        return {
            'mapping_stats': self.mapping_stats,
            'correction_success_rate': correction_success_rate,
            'pattern_stats': pattern_stats,
            'total_patterns': len(self.error_patterns)
        }
    
    def get_most_common_errors(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Retorna los errores más comunes."""
        sorted_patterns = sorted(
            self.error_patterns,
            key=lambda p: p.occurrence_count,
            reverse=True
        )
        
        return [
            {
                'error_type': pattern.error_type,
                'category': pattern.category.value,
                'severity': pattern.severity.value,
                'occurrence_count': pattern.occurrence_count,
                'success_rate': pattern.get_success_rate(),
                'last_seen': pattern.last_seen.isoformat() if pattern.last_seen else None
            }
            for pattern in sorted_patterns[:limit]
        ]
    
    def add_custom_pattern(self, pattern: ErrorPattern):
        """Agrega un patrón de error personalizado."""
        self.error_patterns.append(pattern)
        logger.info(f"Patrón personalizado agregado: {pattern.error_type}")
    
    def get_patterns_by_category(self, category: ErrorCategory) -> List[ErrorPattern]:
        """Retorna patrones por categoría."""
        return [p for p in self.error_patterns if p.category == category]
    
    def get_patterns_by_severity(self, severity: ErrorSeverity) -> List[ErrorPattern]:
        """Retorna patrones por severidad."""
        return [p for p in self.error_patterns if p.severity == severity]


if __name__ == "__main__":
    # Test del ErrorMapper
    logging.basicConfig(level=logging.INFO)
    
    mapper = ErrorMapper()
    
    # Test de mapeo de errores
    test_errors = [
        ("SyntaxError", "unexpected EOF while parsing"),
        ("NameError", "name 'x' is not defined"),
        ("TypeError", "can only concatenate str (not 'int') to str"),
        ("IndentationError", "expected an indented block"),
        ("ImportError", "No module named 'numpy'"),
        ("AttributeError", "'NoneType' object has no attribute 'append'"),
        ("IndexError", "list index out of range"),
        ("KeyError", "'username'")
    ]
    
    for error_type, error_message in test_errors:
        pattern = mapper.map_error(error_message, error_type, "", "python")
        if pattern:
            strategy = mapper.get_correction_strategy(error_message, error_type, "", "python")
            print(f"{error_type}: {error_message}")
            print(f"  Pattern: {pattern.error_type}")
            print(f"  Strategy: {strategy['name'] if strategy else 'None'}")
            print(f"  Confidence: {strategy['confidence'] if strategy else 'N/A'}")
            print()
    
    # Mostrar estadísticas
    stats = mapper.get_error_statistics()
    print(f"Estadísticas: {stats}")
    
    # Errores más comunes
    common_errors = mapper.get_most_common_errors(5)
    print(f"\nErrores más comunes:")
    for error in common_errors:
        print(f"  {error['error_type']}: {error['occurrence_count']} ocurrencias")
