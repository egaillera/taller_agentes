# CSV Data Analyst Agent - Workshop

Un agente de IA construido con **Langgraph** que puede analizar datasets CSV mediante consultas en lenguaje natural.

Este proyecto es parte de un workshop de 90 minutos sobre agentes de IA para estudiantes de Master en Big Data y Análisis de Datos.

## Descripción del Proyecto

El agente CSV Data Analyst es capaz de:
- Cargar y describir archivos CSV para entender su estructura
- Calcular estadísticas descriptivas (media, mediana, desviación estándar, etc.)
- Crear visualizaciones (histogramas) de la distribución de datos
- Razonar de forma autónoma sobre qué herramientas usar para responder consultas

## Estructura del Proyecto

```
csv_agent/
├── .env.example           # Ejemplo de configuración de variables de entorno
├── requirements.txt       # Dependencias de Python
├── crear_dataset.py       # Script para generar el dataset de ejemplo
├── ventas.csv            # Dataset de ejemplo (generado)
├── codigo_base.py        # Plantilla inicial (para completar en el workshop)
├── solucion_completa.py  # Solución completa funcional
├── plots/                # Directorio para gráficas (se crea automáticamente)
└── README.md            # Este archivo
```

## Instalación

### 1. Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Una cuenta en OpenAI con acceso a la API

### 2. Clonar o Descargar el Proyecto

```bash
# Si usas git
git clone <url-del-repositorio>
cd csv_agent

# O simplemente descarga y descomprime el archivo ZIP
```

### 3. Crear un Entorno Virtual (Recomendado)

```bash
# En macOS/Linux
python3 -m venv venv
source venv/bin/activate

# En Windows
python -m venv venv
venv\Scripts\activate
```

### 4. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 5. Configurar la API Key de OpenAI

1. Copia el archivo de ejemplo:
   ```bash
   cp .env.example .env
   ```

2. Edita el archivo `.env` y añade tu API key:
   ```
   OPENAI_API_KEY=sk-tu-api-key-aqui
   ```

3. Para obtener una API key:
   - Ve a https://platform.openai.com/api-keys
   - Inicia sesión o crea una cuenta
   - Crea una nueva API key
   - Copia la key y pégala en el archivo `.env`

**IMPORTANTE:** Nunca compartas tu API key ni la subas a repositorios públicos.

## Uso

### Paso 1: Generar el Dataset de Ejemplo

Primero, genera el archivo `ventas.csv` con datos de ejemplo:

```bash
python crear_dataset.py
```

Este script creará un archivo CSV con 100 filas de datos de ventas ficticias, incluyendo:
- Productos
- Precios (distribución normal)
- Cantidades
- Categorías (Electrónica, Ropa, Alimentos, Hogar, Deportes)
- Fechas (100 días consecutivos)

**Salida esperada:**
```
🔧 Generando dataset de ventas...

✓ Generados 100 productos
✓ Generados precios (rango: 11.23 - 89.45)
✓ Generadas cantidades (rango: 1 - 100)
✓ Asignadas categorías: Electrónica, Ropa, Alimentos, Hogar, Deportes
✓ Generadas fechas (2024-01-01 a 2024-04-09)

✅ Dataset creado exitosamente: ventas.csv
```

### Paso 2: Ejecutar el Código Base (Workshop)

Durante el workshop, trabajarás con `codigo_base.py`:

```bash
python codigo_base.py
```

**Nota:** Este archivo tiene las herramientas sin implementar. Los estudiantes las completarán durante el workshop.

### Paso 3: Ejecutar la Solución Completa

Para ver cómo funciona el agente completamente implementado:

```bash
python solucion_completa.py
```

El agente ejecutará automáticamente 4 casos de prueba:

1. **Exploración básica**: Dimensiones y columnas del dataset
2. **Estadísticas**: Media y desviación estándar de precios
3. **Visualización**: Histograma de la columna 'precio'
4. **Análisis completo**: Combinación de múltiples herramientas

**Ejemplo de salida:**
```
🤖 CSV DATA ANALYST AGENT - DEMO
================================================================================

📌 TEST 1: Exploración básica del dataset
================================================================================
📝 CONSULTA: How many rows and columns does ventas.csv have? What columns does it contain?
================================================================================

💭 RAZONAMIENTO (Paso 1):
   I need to load and describe the CSV file to answer this question.

🔧 USANDO HERRAMIENTA: load_and_describe_csv
   Argumentos: {'filepath': 'ventas.csv'}

📊 RESULTADO DE HERRAMIENTA:
   📊 INFORMACIÓN DEL DATASET: ventas.csv

   📏 Dimensiones: 100 filas x 5 columnas
   ...

✅ RESPUESTA FINAL:
   The ventas.csv file has 100 rows and 5 columns. The columns are: producto, precio, cantidad, categoria, and fecha.
```

## Flujo del Workshop

### Fase 1: Configuración (10 minutos)
- Instalar dependencias
- Configurar API key
- Generar dataset
- Explicar la arquitectura del agente

### Fase 2: Teoría (15 minutos)
- ¿Qué son los agentes de IA?
- Arquitectura ReAct (Reasoning + Acting)
- Langgraph y su ciclo de ejecución
- Cómo funcionan las herramientas (tools)

### Fase 3: Implementación (50 minutos)
- **Tarea 1** (10 min): Completar el system prompt
- **Tarea 2** (15 min): Implementar `load_and_describe_csv`
- **Tarea 3** (15 min): Implementar `get_statistics`
- **Tarea 4** (10 min): Implementar `plot_distribution`

### Fase 4: Pruebas y Demostración (15 minutos)
- Ejecutar los casos de prueba
- Analizar el razonamiento del agente
- Discutir mejoras posibles
- Q&A

## Archivos del Proyecto

### `codigo_base.py`
Plantilla inicial para el workshop. Contiene:
- Imports y configuración completa
- System prompt parcial (estudiantes lo completan)
- Tres herramientas sin implementar (con hints detallados)
- Agente ya configurado
- Función `run_agent` que muestra el razonamiento
- Casos de prueba listos

### `solucion_completa.py`
Solución completa y funcional. Incluye:
- System prompt completo
- Todas las herramientas implementadas con manejo de errores
- Misma estructura que `codigo_base.py`

### `crear_dataset.py`
Script para generar datos de ejemplo:
- 100 filas de datos de ventas
- Distribución realista de precios
- Múltiples categorías
- Fechas secuenciales

## Conceptos Clave

### 1. Agentes ReAct
El patrón **ReAct** (Reasoning + Acting) permite al agente:
1. **Razonar** sobre qué hacer
2. **Actuar** usando herramientas
3. **Observar** los resultados
4. Repetir hasta completar la tarea

### 2. Herramientas (Tools)
Las herramientas son funciones que el agente puede llamar:
- Decoradas con `@tool`
- Tienen docstrings descriptivos (el agente los lee)
- Reciben parámetros tipados
- Retornan strings con resultados

### 3. Langgraph
Framework para construir agentes con grafos de estado:
- `create_react_agent`: Crea un agente ReAct preconfigurado
- `agent.stream()`: Ejecuta el agente y retorna cada paso
- Maneja el ciclo razonamiento → acción → observación

## Troubleshooting

### Error: "OPENAI_API_KEY no encontrada"

**Problema:** No se configuró la API key.

**Solución:**
1. Crea un archivo `.env` en el directorio del proyecto
2. Añade: `OPENAI_API_KEY=tu-clave-aqui`
3. Verifica que el archivo `.env` esté en el mismo directorio que los scripts

### Error: "ModuleNotFoundError: No module named 'langgraph'"

**Problema:** Las dependencias no están instaladas.

**Solución:**
```bash
pip install -r requirements.txt
```

### Error: "FileNotFoundError: ventas.csv"

**Problema:** El dataset no ha sido generado.

**Solución:**
```bash
python crear_dataset.py
```

### Error: "RateLimitError" de OpenAI

**Problema:** Has excedido el límite de requests de tu API key.

**Solución:**
- Espera unos minutos antes de intentar de nuevo
- Verifica tu plan en OpenAI (https://platform.openai.com/usage)
- Considera usar `gpt-4o-mini` en lugar de modelos más grandes (ya está configurado)

### Las gráficas no se generan

**Problema:** El directorio `plots/` no existe o no hay permisos.

**Solución:**
- El directorio se crea automáticamente al ejecutar el código
- Verifica permisos de escritura en el directorio del proyecto
- En Linux/Mac: `chmod +w .`

### Error: "Tool not working" en codigo_base.py

**Problema:** Las herramientas en `codigo_base.py` no están implementadas.

**Solución:**
- Este es el comportamiento esperado - las herramientas tienen `pass`
- Los estudiantes deben implementarlas durante el workshop
- Para ver la versión funcional, usa `solucion_completa.py`

## Extensiones Posibles

Ideas para extender el proyecto:

1. **Más herramientas:**
   - `filter_data`: Filtrar filas por condiciones
   - `group_by`: Agrupar y agregar datos
   - `plot_scatter`: Gráficos de dispersión
   - `plot_time_series`: Series temporales

2. **Mejores visualizaciones:**
   - Usar seaborn para gráficos más elaborados
   - Gráficos interactivos con plotly
   - Múltiples subplots

3. **Análisis avanzado:**
   - Detección de outliers
   - Correlaciones entre columnas
   - Modelos predictivos simples

4. **Interfaz de usuario:**
   - Streamlit para interfaz web
   - Gradio para demos rápidas
   - CLI interactiva con rich

5. **Múltiples datasets:**
   - Cargar varios CSVs
   - Joins entre datasets
   - Comparaciones

## Recursos Adicionales

- **Langgraph Documentation:** https://langchain-ai.github.io/langgraph/
- **LangChain Documentation:** https://python.langchain.com/
- **OpenAI API Documentation:** https://platform.openai.com/docs
- **Pandas Documentation:** https://pandas.pydata.org/docs/
- **Matplotlib Gallery:** https://matplotlib.org/stable/gallery/

## Licencia

Este proyecto es material educativo para workshops. Libre uso con atribución.

## Contacto

Para preguntas sobre el workshop o el código, contacta con el instructor.

---

**¡Disfruta del workshop y construye agentes increíbles!** 🤖✨
