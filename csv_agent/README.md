# CSV Data Analyst Agent - Workshop

Un agente de IA construido con **Langgraph** que puede analizar datasets CSV mediante consultas en lenguaje natural.


## Descripción del Proyecto

El agente CSV Data Analyst es capaz de:
- Cargar y describir archivos CSV para entender su estructura
- Calcular estadísticas descriptivas (media, mediana, desviación estándar, etc.)
- Crear visualizaciones (histogramas) de la distribución de datos
- Razonar de forma autónoma sobre qué herramientas usar para responder consultas

## 🔑 Guía para Obtener tu API Key de Gemini

**IMPORTANTE:** Antes de empezar con la instalación, necesitas una API key de Google Gemini. Sigue estos pasos utilizando tu cuenta de Google (Gmail):

### Paso 1: Acceder a Google AI Studio

1. Abre tu navegador y dirígete a **[aistudio.google.com](https://aistudio.google.com)**

2. Si no has iniciado sesión:
   - Introduce tu correo de Google (Gmail)
   - Introduce tu contraseña

3. **Nota importante:** La primera vez que entres, deberás aceptar los **Términos de Servicio**
   - Asegúrate de marcar las casillas correspondientes para continuar
   - Lee los términos y acepta para proceder

### Paso 2: Generar la API Key

Una vez dentro del panel principal de Google AI Studio:

1. En el **menú lateral izquierdo**, busca y haz clic en el botón que dice **"Get API key"**
   - Tiene un icono de una llave 🔑

2. Se abrirá una ventana central
   - Haz clic en el **botón azul** que dice **"Create API key in new project"**
   - Esto creará automáticamente un contenedor en Google Cloud para tu llave
   - **No necesitas configurar nada manualmente**

3. Espera unos segundos a que se genere el código alfanumérico

### Paso 3: Copiar y Guardar tu API Key

1. Aparecerá una ventana con tu clave (un texto largo con letras y números que comienza con `AIza...`)

2. Haz clic en el botón **"Copy"** para copiar la clave

3. **¡MUY IMPORTANTE!**
   - Pega esa clave en un bloc de notas o un gestor de contraseñas
   - **Guárdala de forma segura** - la necesitarás en el paso de configuración
   - **Nunca compartas esta clave** ni la subas a repositorios públicos

### ✅ Listo para Continuar

Una vez que tengas tu API key copiada y guardada, estás listo para continuar con la instalación del proyecto.

---

## Estructura del Proyecto

```
csv_agent/
├── .env.example          # Ejemplo de configuración de variables de entorno
├── requirements.txt      # Dependencias de Python
├── ventas.csv            # Dataset de ejemplo (generado)
├── codigo_base.py        # Plantilla inicial (para completar en el workshop)
├── plots/                # Directorio para gráficas (se crea automáticamente)
└── README.md             # Este archivo
```

## Instalación

### 1. Requisitos Previos

- Python 3.8 o superior, pero inferior a 3.14
- pip (gestor de paquetes de Python)
- Una cuenta de Google con acceso a la API de Gemini (gratuita)

### 2. Clonar o Descargar el Proyecto

```bash
# Si usas git
git clone https://github.com/egaillera/taller_agentes/
cd taller_agentes/csv_agent

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

### 5. Configurar la API Key de Google Gemini

1. Copia el archivo de ejemplo:
   ```bash
   cp .env.example .env
   ```

2. Edita el archivo `.env` y añade tu API key:
   ```
   GOOGLE_API_KEY=tu-api-key-de-google-aqui
   ```


## Troubleshooting

### Error: "GOOGLE_API_KEY no encontrada"

**Problema:** No se configuró la API key.

**Solución:**
1. Crea un archivo `.env` en el directorio del proyecto
2. Añade: `GOOGLE_API_KEY=tu-clave-aqui`
3. Verifica que el archivo `.env` esté en el mismo directorio que los scripts
4. Obtén tu API key gratuita en: https://aistudio.google.com/app/apikey

### Error: "ModuleNotFoundError: No module named 'langgraph'"

**Problema:** Las dependencias no están instaladas.

**Solución:**
```bash
pip install -r requirements.txt
```

### Error: "RateLimitError" de Google

**Problema:** Has excedido el límite de requests de tu API key.

**Solución:**
- Espera unos minutos antes de intentar de nuevo
- El tier gratuito de Google Gemini es muy generoso (60 requests por minuto)
- Verifica tu uso en: https://aistudio.google.com/
- El modelo `gemini-2.5-flash` ya está configurado en el código

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
- **Google Gemini API Documentation:** https://ai.google.dev/docs
- **Google AI Studio:** https://aistudio.google.com/
- **Pandas Documentation:** https://pandas.pydata.org/docs/
- **Matplotlib Gallery:** https://matplotlib.org/stable/gallery/


---


