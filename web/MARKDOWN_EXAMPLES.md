# Ejemplos de Formato Markdown - Capibara6 Chat

El chat ahora soporta **Markdown completo** con syntax highlighting y tablas. El modelo puede usar estos formatos en sus respuestas.

## 📊 Tablas

### Ejemplo 1: Tabla de Usuarios
```markdown
| name | gender | country | username | model | status_code |
|------|--------|---------|----------|-------|-------------|
| john doe | Male | US | jdoe | v1.0 | 200 |
| jane smith | Female | UK | jsmith | v2.0 | 200 |
| bob jones | Male | CA | bjones | v1.5 | 404 |
```

**Resultado:**
| name | gender | country | username | model | status_code |
|------|--------|---------|----------|-------|-------------|
| john doe | Male | US | jdoe | v1.0 | 200 |
| jane smith | Female | UK | jsmith | v2.0 | 200 |
| bob jones | Male | CA | bjones | v1.5 | 404 |

### Ejemplo 2: Tabla de Comparación
```markdown
| Feature | Plan Free | Plan Pro | Plan Enterprise |
|---------|-----------|----------|-----------------|
| Usuarios | 1 | 10 | Ilimitado |
| Storage | 1GB | 100GB | 1TB |
| Soporte | Email | 24/7 | Dedicado |
| Precio | $0 | $10/mes | Custom |
```

## 💻 Código con Syntax Highlighting

### Python
```markdown
\`\`\`python
def process_data(data):
    result = []
    for item in data:
        if item['status'] == 200:
            result.append(item)
    return result
\`\`\`
```

### JavaScript
```markdown
\`\`\`javascript
const fetchData = async (url) => {
  try {
    const response = await fetch(url);
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error:', error);
  }
};
\`\`\`
```

### SQL
```markdown
\`\`\`sql
SELECT name, gender, country
FROM users
WHERE status_code = 200
ORDER BY name ASC;
\`\`\`
```

### Bash
```markdown
\`\`\`bash
curl http://34.175.89.158:8080/completion -d '{
  "prompt": "hello",
  "n_predict": 128
}'
\`\`\`
```

## 📝 Listas

### Lista sin orden
```markdown
- Elemento 1
- Elemento 2
  - Sub-elemento 2.1
  - Sub-elemento 2.2
- Elemento 3
```

### Lista ordenada
```markdown
1. Primer paso
2. Segundo paso
3. Tercer paso
   1. Sub-paso 3.1
   2. Sub-paso 3.2
```

## 🎨 Formato de Texto

```markdown
**Negrita**
*Cursiva*
***Negrita y cursiva***
~~Tachado~~
`código inline`
```

## 📌 Encabezados

```markdown
# Encabezado 1
## Encabezado 2
### Encabezado 3
#### Encabezado 4
```

## 💬 Citas

```markdown
> Esto es una cita
> Puede tener múltiples líneas
>
> Y párrafos separados
```

## 🔗 Enlaces

```markdown
[Texto del enlace](https://ejemplo.com)
[Documentación oficial](https://docs.example.com)
```

## ➖ Línea Horizontal

```markdown
---
```

## 🎯 Ejemplo Completo

El modelo puede combinar todos estos elementos en una respuesta:

```markdown
# Análisis de Datos de Usuarios

## Resultados de la Consulta

La consulta SQL devolvió los siguientes usuarios activos:

| name | gender | country | username | model | status_code |
|------|--------|---------|----------|-------|-------------|
| john doe | Male | US | jdoe | v1.0 | 200 |
| jane smith | Female | UK | jsmith | v2.0 | 200 |

## Código de Implementación

Para procesar estos datos en Python:

\`\`\`python
def filter_active_users(users):
    """Filtra usuarios con status_code 200"""
    return [user for user in users if user['status_code'] == 200]

active_users = filter_active_users(data)
print(f"Total usuarios activos: {len(active_users)}")
\`\`\`

## Pasos Siguientes

1. **Validar datos**: Verificar integridad
2. **Exportar**: Generar reporte CSV
3. **Notificar**: Enviar alertas

> **Nota**: Asegúrate de validar todos los campos antes de procesar.

---

Para más información, consulta la [documentación oficial](https://docs.example.com).
```

## 🛠️ Soporte Técnico

El chat usa:
- **Marked.js v11.1.1**: Para renderizar Markdown
- **Highlight.js v11.9.0**: Para syntax highlighting de código
- **GitHub Dark Theme**: Tema de colores para código

### Lenguajes Soportados para Syntax Highlighting

- Python
- JavaScript / TypeScript
- SQL
- Bash / Shell
- HTML / CSS
- JSON
- Java
- C / C++
- Ruby
- PHP
- Go
- Rust
- Y muchos más...

## 📱 Responsive

Todas las tablas y bloques de código son responsivos:
- Se ajustan al ancho disponible
- Tienen scroll horizontal si es necesario
- Se ven bien en móviles y desktop

