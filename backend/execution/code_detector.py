#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Code Detector - Detecta bloques de código en respuestas y extrae información relevante.
"""

import re
import logging
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime

logger = logging.getLogger(__name__)


class CodeBlock:
    """Representa un bloque de código detectado."""
    
    def __init__(self, 
                 language: str,
                 code: str,
                 start_line: int,
                 end_line: int,
                 context: str = ""):
        self.language = language
        self.code = code.strip()
        self.start_line = start_line
        self.end_line = end_line
        self.context = context
        self.detected_at = datetime.now()
        
        # Análisis del código
        self.line_count = len(self.code.split('\n'))
        self.char_count = len(self.code)
        self.complexity_score = self._calculate_complexity()
        self.requires_execution = self._should_execute()
        
    def _calculate_complexity(self) -> float:
        """Calcula un score de complejidad del código."""
        score = 0.0
        
        # Factores de complejidad
        if 'import' in self.code or 'require' in self.code:
            score += 0.2  # Dependencias
        if 'def ' in self.code or 'function' in self.code:
            score += 0.3  # Funciones
        if 'class ' in self.code:
            score += 0.4  # Clases
        if 'if ' in self.code or 'for ' in self.code or 'while ' in self.code:
            score += 0.2  # Control flow
        if 'try:' in self.code or 'except' in self.code:
            score += 0.3  # Manejo de errores
        if 'async' in self.code or 'await' in self.code:
            score += 0.3  # Asincronía
        
        # Normalizar por longitud
        if self.line_count > 0:
            score = min(1.0, score * (10 / self.line_count))
        
        return score
    
    def _should_execute(self) -> bool:
        """Determina si el código debería ejecutarse."""
        # Código que no debería ejecutarse
        skip_patterns = [
            r'^#',  # Comentarios
            r'^//',  # Comentarios JS
            r'^/\*',  # Comentarios multi-línea
            r'^--',  # Comentarios SQL
            r'^"""',  # Docstrings
            r'^"""',  # Docstrings
        ]
        
        first_line = self.code.split('\n')[0].strip()
        for pattern in skip_patterns:
            if re.match(pattern, first_line):
                return False
        
        # Código que debería ejecutarse
        execute_patterns = [
            r'print\s*\(',  # Python print
            r'console\.log\s*\(',  # JavaScript console.log
            r'SELECT\s+',  # SQL SELECT
            r'INSERT\s+',  # SQL INSERT
            r'UPDATE\s+',  # SQL UPDATE
            r'DELETE\s+',  # SQL DELETE
            r'def\s+\w+\s*\(',  # Python function definition
            r'function\s+\w+\s*\(',  # JavaScript function
            r'class\s+\w+',  # Class definition
        ]
        
        for pattern in execute_patterns:
            if re.search(pattern, self.code, re.IGNORECASE):
                return True
        
        # Si tiene más de 3 líneas, probablemente debería ejecutarse
        return self.line_count > 3
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte el bloque de código a diccionario."""
        return {
            'language': self.language,
            'code': self.code,
            'start_line': self.start_line,
            'end_line': self.end_line,
            'context': self.context,
            'line_count': self.line_count,
            'char_count': self.char_count,
            'complexity_score': self.complexity_score,
            'requires_execution': self.requires_execution,
            'detected_at': self.detected_at.isoformat()
        }


class CodeDetector:
    """Detecta y analiza bloques de código en texto."""
    
    def __init__(self):
        # Patrones para detectar bloques de código markdown
        self.markdown_patterns = {
            'python': r'```python\s*\n(.*?)\n```',
            'javascript': r'```javascript\s*\n(.*?)\n```',
            'js': r'```js\s*\n(.*?)\n```',
            'sql': r'```sql\s*\n(.*?)\n```',
            'bash': r'```bash\s*\n(.*?)\n```',
            'shell': r'```shell\s*\n(.*?)\n```',
            'generic': r'```(\w+)?\s*\n(.*?)\n```'
        }
        
        # Patrones para detectar código inline
        self.inline_patterns = {
            'python': r'`([^`]+)`',
            'javascript': r'`([^`]+)`',
            'sql': r'`([^`]+)`'
        }
        
        # Lenguajes soportados
        self.supported_languages = ['python', 'javascript', 'js', 'sql', 'bash', 'shell']
        
        self.detection_stats = {
            'total_detections': 0,
            'languages_detected': {},
            'execution_candidates': 0,
            'avg_complexity': 0.0
        }
        
        logger.info("CodeDetector inicializado")
    
    def detect_code_blocks(self, text: str) -> List[CodeBlock]:
        """
        Detecta todos los bloques de código en el texto.
        
        Args:
            text: Texto a analizar
            
        Returns:
            Lista de CodeBlock detectados
        """
        logger.debug(f"Detectando bloques de código en texto de {len(text)} caracteres")
        
        code_blocks = []
        lines = text.split('\n')
        
        # Detectar bloques markdown
        markdown_blocks = self._detect_markdown_blocks(text, lines)
        code_blocks.extend(markdown_blocks)
        
        # Detectar código inline
        inline_blocks = self._detect_inline_blocks(text, lines)
        code_blocks.extend(inline_blocks)
        
        # Detectar código sin markdown (heurística)
        heuristic_blocks = self._detect_heuristic_blocks(text, lines)
        code_blocks.extend(heuristic_blocks)
        
        # Actualizar estadísticas
        self._update_detection_stats(code_blocks)
        
        logger.info(f"Detectados {len(code_blocks)} bloques de código")
        return code_blocks
    
    def _detect_markdown_blocks(self, text: str, lines: List[str]) -> List[CodeBlock]:
        """Detecta bloques de código markdown."""
        blocks = []
        
        for language, pattern in self.markdown_patterns.items():
            matches = re.finditer(pattern, text, re.DOTALL | re.IGNORECASE)
            
            for match in matches:
                if language == 'generic':
                    # Patrón genérico captura el lenguaje
                    detected_lang = match.group(1) or 'unknown'
                    code = match.group(2)
                else:
                    detected_lang = language
                    code = match.group(1)
                
                # Encontrar líneas de inicio y fin
                start_line = text[:match.start()].count('\n') + 1
                end_line = text[:match.end()].count('\n') + 1
                
                # Obtener contexto
                context = self._extract_context(lines, start_line, end_line)
                
                block = CodeBlock(
                    language=detected_lang,
                    code=code,
                    start_line=start_line,
                    end_line=end_line,
                    context=context
                )
                
                blocks.append(block)
        
        return blocks
    
    def _detect_inline_blocks(self, text: str, lines: List[str]) -> List[CodeBlock]:
        """Detecta código inline (entre backticks)."""
        blocks = []
        
        # Patrón para código inline
        inline_pattern = r'`([^`\n]+)`'
        matches = re.finditer(inline_pattern, text)
        
        for match in matches:
            code = match.group(1)
            
            # Determinar lenguaje basado en el contexto
            language = self._detect_language_from_context(code, match.start(), text)
            
            # Solo incluir si parece ser código ejecutable
            if self._is_executable_inline(code, language):
                start_line = text[:match.start()].count('\n') + 1
                end_line = start_line
                
                context = self._extract_context(lines, start_line, end_line)
                
                block = CodeBlock(
                    language=language,
                    code=code,
                    start_line=start_line,
                    end_line=end_line,
                    context=context
                )
                
                blocks.append(block)
        
        return blocks
    
    def _detect_heuristic_blocks(self, text: str, lines: List[str]) -> List[CodeBlock]:
        """Detecta código usando heurísticas (sin markdown)."""
        blocks = []
        
        # Patrones heurísticos para diferentes lenguajes
        heuristic_patterns = {
            'python': [
                r'def\s+\w+\s*\([^)]*\):',
                r'class\s+\w+[^:]*:',
                r'import\s+\w+',
                r'from\s+\w+\s+import',
                r'if\s+__name__\s*==\s*["\']__main__["\']:'
            ],
            'javascript': [
                r'function\s+\w+\s*\([^)]*\)\s*{',
                r'const\s+\w+\s*=\s*\([^)]*\)\s*=>',
                r'let\s+\w+\s*=',
                r'var\s+\w+\s*=',
                r'console\.log\s*\('
            ],
            'sql': [
                r'SELECT\s+.*\s+FROM\s+',
                r'INSERT\s+INTO\s+',
                r'UPDATE\s+\w+\s+SET\s+',
                r'DELETE\s+FROM\s+',
                r'CREATE\s+TABLE\s+'
            ]
        }
        
        for language, patterns in heuristic_patterns.items():
            for pattern in patterns:
                matches = re.finditer(pattern, text, re.IGNORECASE)
                
                for match in matches:
                    # Extraer bloque de código alrededor del match
                    code_block = self._extract_code_block_around_match(text, match, language)
                    
                    if code_block and len(code_block.strip()) > 10:  # Mínimo de caracteres
                        start_line = text[:match.start()].count('\n') + 1
                        end_line = text[:match.end()].count('\n') + 1
                        
                        context = self._extract_context(lines, start_line, end_line)
                        
                        block = CodeBlock(
                            language=language,
                            code=code_block,
                            start_line=start_line,
                            end_line=end_line,
                            context=context
                        )
                        
                        # Solo agregar si parece ser código válido
                        if block.requires_execution and block.complexity_score > 0.1:
                            blocks.append(block)
        
        return blocks
    
    def _extract_code_block_around_match(self, text: str, match, language: str) -> str:
        """Extrae un bloque de código alrededor de un match."""
        start = match.start()
        end = match.end()
        
        # Expandir hacia atrás y adelante para capturar el bloque completo
        lines = text.split('\n')
        match_start_line = text[:start].count('\n')
        match_end_line = text[:end].count('\n')
        
        # Buscar inicio del bloque (línea vacía o indentación)
        block_start = match_start_line
        for i in range(match_start_line - 1, -1, -1):
            line = lines[i].strip()
            if not line or line.startswith('#') or line.startswith('//'):
                block_start = i + 1
                break
            if i < match_start_line - 1 and not line.startswith(' ') and not line.startswith('\t'):
                break
        
        # Buscar fin del bloque
        block_end = match_end_line
        for i in range(match_end_line + 1, len(lines)):
            line = lines[i].strip()
            if not line:
                block_end = i
                break
            if not line.startswith(' ') and not line.startswith('\t') and not line.startswith('#'):
                if language == 'python' and ':' in line:
                    continue  # Continuar para bloques Python
                break
        
        # Extraer el bloque
        block_lines = lines[block_start:block_end + 1]
        return '\n'.join(block_lines)
    
    def _detect_language_from_context(self, code: str, position: int, text: str) -> str:
        """Detecta el lenguaje basado en el contexto."""
        # Buscar pistas en el texto circundante
        context_start = max(0, position - 200)
        context_end = min(len(text), position + 200)
        context = text[context_start:context_end].lower()
        
        # Palabras clave que indican lenguaje
        language_keywords = {
            'python': ['python', 'def ', 'import ', 'from ', 'print('],
            'javascript': ['javascript', 'js', 'function', 'const ', 'let ', 'var '],
            'sql': ['sql', 'select', 'from ', 'where ', 'insert', 'update'],
            'bash': ['bash', 'shell', '#!/bin/', 'echo ', 'ls ', 'cd ']
        }
        
        for language, keywords in language_keywords.items():
            for keyword in keywords:
                if keyword in context:
                    return language
        
        # Análisis del código mismo
        if 'def ' in code or 'import ' in code or 'print(' in code:
            return 'python'
        elif 'function' in code or 'const ' in code or 'console.log' in code:
            return 'javascript'
        elif 'SELECT' in code.upper() or 'FROM' in code.upper():
            return 'sql'
        elif 'echo ' in code or 'ls ' in code or 'cd ' in code:
            return 'bash'
        
        return 'unknown'
    
    def _is_executable_inline(self, code: str, language: str) -> bool:
        """Determina si código inline es ejecutable."""
        # Código muy corto probablemente no es ejecutable
        if len(code.strip()) < 5:
            return False
        
        # Patrones que indican código ejecutable
        executable_patterns = {
            'python': [r'print\s*\(', r'def\s+\w+', r'import\s+\w+', r'[a-zA-Z_]\w*\s*\('],
            'javascript': [r'console\.log\s*\(', r'function\s+\w+', r'[a-zA-Z_]\w*\s*\('],
            'sql': [r'SELECT\s+', r'INSERT\s+', r'UPDATE\s+', r'DELETE\s+'],
            'bash': [r'echo\s+', r'ls\s+', r'cd\s+', r'[a-zA-Z_]\w*\s+']
        }
        
        patterns = executable_patterns.get(language, [])
        for pattern in patterns:
            if re.search(pattern, code, re.IGNORECASE):
                return True
        
        return False
    
    def _extract_context(self, lines: List[str], start_line: int, end_line: int) -> str:
        """Extrae contexto alrededor de un bloque de código."""
        context_start = max(0, start_line - 3)
        context_end = min(len(lines), end_line + 3)
        
        context_lines = []
        for i in range(context_start, context_end):
            if i < len(lines):
                prefix = ">>> " if start_line <= i <= end_line else "    "
                context_lines.append(f"{prefix}{lines[i]}")
        
        return '\n'.join(context_lines)
    
    def _update_detection_stats(self, blocks: List[CodeBlock]):
        """Actualiza estadísticas de detección."""
        self.detection_stats['total_detections'] += len(blocks)
        
        for block in blocks:
            # Estadísticas por lenguaje
            if block.language not in self.detection_stats['languages_detected']:
                self.detection_stats['languages_detected'][block.language] = 0
            self.detection_stats['languages_detected'][block.language] += 1
            
            # Contar candidatos para ejecución
            if block.requires_execution:
                self.detection_stats['execution_candidates'] += 1
        
        # Calcular complejidad promedio
        if blocks:
            total_complexity = sum(block.complexity_score for block in blocks)
            self.detection_stats['avg_complexity'] = total_complexity / len(blocks)
    
    def get_execution_candidates(self, text: str) -> List[CodeBlock]:
        """Retorna solo los bloques de código que deberían ejecutarse."""
        all_blocks = self.detect_code_blocks(text)
        return [block for block in all_blocks if block.requires_execution]
    
    def get_stats(self) -> Dict[str, Any]:
        """Retorna estadísticas del detector."""
        return {
            'detection_stats': self.detection_stats,
            'supported_languages': self.supported_languages
        }


if __name__ == "__main__":
    # Test del CodeDetector
    logging.basicConfig(level=logging.INFO)
    
    detector = CodeDetector()
    
    # Test con texto que contiene código
    test_text = """
    Aquí tienes un ejemplo de función en Python:
    
    ```python
    def greet(name):
        print(f"Hello, {name}!")
        return f"Greeting sent to {name}"
    
    # Uso de la función
    result = greet("World")
    ```
    
    También puedes usar JavaScript:
    
    ```javascript
    function calculateSum(a, b) {
        return a + b;
    }
    
    console.log(calculateSum(5, 3));
    ```
    
    Y aquí una consulta SQL:
    
    ```sql
    SELECT name, email 
    FROM users 
    WHERE active = true;
    ```
    
    También hay código inline como `print("test")` y `SELECT * FROM table`.
    """
    
    # Detectar bloques
    blocks = detector.detect_code_blocks(test_text)
    
    print(f"Bloques detectados: {len(blocks)}")
    for i, block in enumerate(blocks):
        print(f"\nBloque {i+1}:")
        print(f"  Lenguaje: {block.language}")
        print(f"  Líneas: {block.start_line}-{block.end_line}")
        print(f"  Complejidad: {block.complexity_score:.2f}")
        print(f"  Ejecutar: {block.requires_execution}")
        print(f"  Código: {block.code[:100]}...")
    
    # Candidatos para ejecución
    candidates = detector.get_execution_candidates(test_text)
    print(f"\nCandidatos para ejecución: {len(candidates)}")
    
    # Estadísticas
    stats = detector.get_stats()
    print(f"\nEstadísticas: {stats}")
