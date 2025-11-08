## Servidores Legacy

Este directorio agrupa implementaciones antiguas del backend que se mantienen
solo con fines de referencia histórica. Ninguno de estos scripts forma parte
del pipeline actual (`backend/server.py` + `ollama_client.py` + `task_classifier.py`).

Antes de reutilizar cualquiera de estos archivos, revisa si la funcionalidad
ya está cubierta por el backend moderno o si conviene portar la lógica a los
módulos activos.

Ficheros principales:

- `capibara6_integrated_server.py`: versión monolítica previa al enrutador multi-modelo.
- `consensus_server.py`: servidor Flask para consenso entre modelos legacy.
- `coqui_tts_server*.py`: integraciones antiguas de TTS (reemplazadas por Kyutai).
- `kyutai_tts_server*.py`: prototipos iniciales de streaming TTS.
- `smart_mcp_*`: “Smart MCP” experimental; sustituido por `backend/mcp_connector.py`.
- `server_gptoss.py`, `start_*`: scripts de arranque específicos ya cubiertos por `server.py`.

