"""
TOON Utils - Token-Oriented Object Notation
Formato compacto para reducir uso de tokens en LLMs
"""

from .parser import ToonParser
from .encoder import ToonEncoder
from .format_manager import FormatManager

__version__ = "1.0.0"
__all__ = ["ToonParser", "ToonEncoder", "FormatManager"]
