"""
CSV Data Analyst Agent - Código Base para el Workshop

Este es el código base que los estudiantes completarán durante el workshop.
El agente puede analizar datasets CSV mediante consultas en lenguaje natural.

Workshop: Agentes AI con Langgraph
Autor: Workshop AI Agents
"""

# ============================================
# IMPORTS Y CONFIGURACIÓN INICIAL
# ============================================

from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Usar backend no-interactivo para evitar problemas con threads
import matplotlib.pyplot as plt
from pathlib import Path
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# Verificar que la API key está configurada
if not os.getenv("GOOGLE_API_KEY"):
    raise ValueError(
        "❌ Error: GOOGLE_API_KEY no encontrada.\n"
        "Por favor, crea un archivo .env con tu API key:\n"
        "GOOGLE_API_KEY=tu-clave-aqui\n"
        "Obtén tu API key en: https://aistudio.google.com/app/apikey"
    )

# Crear directorio para guardar las gráficas
PLOTS_DIR = Path("plots")
PLOTS_DIR.mkdir(exist_ok=True)

print("✅ Entorno configurado correctamente")
print(f"📁 Directorio para gráficas: {PLOTS_DIR.absolute()}\n")


# ============================================
# TAREA 1: Completar este system prompt
# ============================================

SYSTEM_PROMPT = """
You are a data analysis assistant expert in analyzing CSV datasets.

Your capabilities:
- [ESTUDIANTES: Agregar más capacidades aquí]

When the user asks you to analyze data:
- [ESTUDIANTES: Agregar directrices aquí]

Always be clear and concise in your responses.
"""


# ============================================
# HERRAMIENTAS (TOOLS) DEL AGENTE
# ============================================

@tool
def load_and_describe_csv(filepath: str) -> str:
    """
    Carga un archivo CSV y retorna información básica sobre el dataset.

    Esta herramienta es útil para entender la estructura del dataset antes
    de realizar análisis más profundos.

    Args:
        filepath: Ruta al archivo CSV que se desea analizar

    Returns:
        String con información sobre el dataset:
        - Dimensiones (filas x columnas)
        - Nombres de las columnas
        - Tipos de datos de cada columna
        - Primeras filas del dataset
    """
    # TODO: Implementar esta función
    #
    # PISTAS:
    # 1. Usa pd.read_csv(filepath) para cargar el archivo
    # 2. Obtén las dimensiones con df.shape (retorna tupla: filas, columnas)
    # 3. Obtén los nombres de columnas con df.columns
    # 4. Obtén los tipos de datos con df.dtypes
    # 5. Obtén las primeras filas con df.head(3)
    # 6. Formatea toda la información en un string claro y legible
    # 7. Maneja posibles errores (archivo no existe, CSV inválido)
    #
    # ESTRUCTURA SUGERIDA:
    # try:
    #     df = pd.read_csv(filepath)
    #     filas, columnas = df.shape
    #     info = f"Dataset: {filepath}\n"
    #     info += f"Dimensiones: {filas} filas x {columnas} columnas\n"
    #     ... (agregar más información)
    #     return info
    # except FileNotFoundError:
    #     return f"Error: El archivo {filepath} no existe"
    # except Exception as e:
    #     return f"Error al cargar el archivo: {str(e)}"

    pass


@tool
def get_statistics(filepath: str, column: str) -> str:
    """
    Calcula estadísticas descriptivas para una columna numérica del dataset.

    Esta herramienta proporciona un resumen estadístico completo de una columna,
    incluyendo medidas de tendencia central, dispersión y distribución.

    Args:
        filepath: Ruta al archivo CSV
        column: Nombre de la columna para la cual calcular estadísticas

    Returns:
        String con estadísticas descriptivas:
        - Media (promedio)
        - Mediana (valor central)
        - Desviación estándar
        - Mínimo y máximo
        - Cuartiles (Q1, Q3)
        - Conteo de valores
    """
    # TODO: Implementar esta función
    #
    # PISTAS:
    # 1. Carga el CSV con pd.read_csv(filepath)
    # 2. Verifica que la columna existe en df.columns
    # 3. Verifica que la columna es numérica (df[column].dtype)
    # 4. Usa df[column].describe() para obtener estadísticas
    # 5. El método describe() retorna: count, mean, std, min, 25%, 50%, 75%, max
    # 6. Formatea las estadísticas de manera clara y legible
    # 7. Maneja errores: archivo no existe, columna no existe, columna no numérica
    #
    # ESTRUCTURA SUGERIDA:
    # try:
    #     df = pd.read_csv(filepath)
    #     if column not in df.columns:
    #         return f"Error: La columna '{column}' no existe"
    #     if not pd.api.types.is_numeric_dtype(df[column]):
    #         return f"Error: La columna '{column}' no es numérica"
    #
    #     stats = df[column].describe()
    #     result = f"Estadísticas para '{column}':\n"
    #     result += f"Media: {stats['mean']:.2f}\n"
    #     ... (agregar más estadísticas)
    #     return result
    # except Exception as e:
    #     return f"Error: {str(e)}"

    pass


@tool
def plot_distribution(filepath: str, column: str) -> str:
    """
    Crea un histograma para visualizar la distribución de una columna numérica.

    Esta herramienta genera una visualización que muestra cómo se distribuyen
    los valores en la columna especificada, guardando el gráfico como imagen.

    Args:
        filepath: Ruta al archivo CSV
        column: Nombre de la columna para visualizar

    Returns:
        String con mensaje de confirmación y la ruta donde se guardó el gráfico
    """
    # TODO: Implementar esta función
    #
    # PISTAS:
    # 1. Carga el CSV con pd.read_csv(filepath)
    # 2. Verifica que la columna existe y es numérica
    # 3. Crea una figura con plt.figure(figsize=(10, 6))
    # 4. Crea el histograma con plt.hist(df[column], bins=20, edgecolor='black')
    # 5. Añade título con plt.title(f'Distribución de {column}')
    # 6. Añade etiquetas con plt.xlabel(column) y plt.ylabel('Frecuencia')
    # 7. Añade grid con plt.grid(True, alpha=0.3)
    # 8. Guarda con plt.savefig(PLOTS_DIR / f'{column}_histogram.png')
    # 9. Cierra la figura con plt.close() para liberar memoria
    # 10. Retorna mensaje con la ruta del archivo guardado
    #
    # ESTRUCTURA SUGERIDA:
    # try:
    #     df = pd.read_csv(filepath)
    #     if column not in df.columns:
    #         return f"Error: La columna '{column}' no existe"
    #     if not pd.api.types.is_numeric_dtype(df[column]):
    #         return f"Error: La columna '{column}' no es numérica"
    #
    #     plt.figure(figsize=(10, 6))
    #     plt.hist(df[column], bins=20, edgecolor='black', alpha=0.7)
    #     ... (agregar título, labels, etc.)
    #
    #     output_path = PLOTS_DIR / f'{column}_histogram.png'
    #     plt.savefig(output_path)
    #     plt.close()
    #
    #     return f"Histograma guardado en: {output_path}"
    # except Exception as e:
    #     return f"Error: {str(e)}"

    pass


# ============================================
# CREACIÓN DEL AGENTE - CÓDIGO YA COMPLETO
# ============================================

# Crear el agente usando create_agent de Langchain
# Este agente puede razonar y usar las herramientas de forma autónoma
agent = create_agent(
    model=ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0),
    tools=[load_and_describe_csv, get_statistics, plot_distribution],
    system_prompt=SYSTEM_PROMPT
)

print("🤖 Agente CSV Data Analyst creado correctamente")
print(f"🛠️  Herramientas disponibles: {len([load_and_describe_csv, get_statistics, plot_distribution])}")
print()


# ============================================
# FUNCIÓN PARA EJECUTAR EL AGENTE
# ============================================

def run_agent(query: str) -> str:
    """
    Ejecuta el agente con una consulta del usuario y muestra el proceso de razonamiento.

    Esta función es pedagógica: muestra cada paso que el agente toma para
    responder la consulta, incluyendo su razonamiento y el uso de herramientas.

    Args:
        query: Pregunta o solicitud del usuario en lenguaje natural

    Returns:
        Respuesta final del agente
    """
    print("=" * 80)
    print(f"📝 CONSULTA: {query}")
    print("=" * 80)
    print()

    try:
        # Ejecutar el agente
        # El agente itera hasta encontrar la respuesta final
        result = None
        step_number = 1

        for step in agent.stream({"messages": [("user", query)]}):
            # Cada step contiene el estado actual del agente
            if "agent" in step:
                messages = step["agent"]["messages"]

                for message in messages:
                    # Mostrar el razonamiento del agente
                    if hasattr(message, "content") and message.content:
                        print(f"💭 RAZONAMIENTO (Paso {step_number}):")
                        print(f"   {message.content}")
                        print()

                    # Mostrar llamadas a herramientas
                    if hasattr(message, "tool_calls") and message.tool_calls:
                        for tool_call in message.tool_calls:
                            print(f"🔧 USANDO HERRAMIENTA: {tool_call['name']}")
                            print(f"   Argumentos: {tool_call['args']}")
                            print()

            # Mostrar resultados de las herramientas
            if "tools" in step:
                messages = step["tools"]["messages"]
                for message in messages:
                    if hasattr(message, "content"):
                        print(f"📊 RESULTADO DE HERRAMIENTA:")
                        # Limitar la salida para que sea legible
                        content = message.content
                        if len(content) > 500:
                            content = content[:500] + "..."
                        print(f"   {content}")
                        print()

            step_number += 1
            result = step

        # Extraer y mostrar la respuesta final
        if result and "agent" in result:
            final_messages = result["agent"]["messages"]
            if final_messages:
                final_response = final_messages[-1].content
                print("=" * 80)
                print("✅ RESPUESTA FINAL:")
                print(f"   {final_response}")
                print("=" * 80)
                print("\n")
                return final_response

        return "No se pudo obtener una respuesta del agente"

    except Exception as e:
        error_msg = f"❌ Error al ejecutar el agente: {str(e)}"
        print(error_msg)
        print()
        return error_msg


# ============================================
# CASOS DE PRUEBA
# ============================================

if __name__ == "__main__":
    print("\n")
    print("🤖 CSV DATA ANALYST AGENT - DEMO")
    print("=" * 80)
    print()
    print("Este agente puede analizar datasets CSV mediante lenguaje natural.")
    print("A continuación se ejecutarán 4 casos de prueba:\n")
    input("Presiona ENTER para comenzar...")
    print("\n")

    # Test 1: Exploración básica del dataset
    print("📌 TEST 1: Exploración básica del dataset")
    run_agent("How many rows and columns does ventas.csv have? What columns does it contain?")

    # Test 2: Estadísticas
    print("📌 TEST 2: Cálculo de estadísticas")
    run_agent("What is the average price and standard deviation in ventas.csv?")

    # Test 3: Visualización
    print("📌 TEST 3: Creación de visualización")
    run_agent("Create a histogram of the 'precio' column from ventas.csv")

    # Test 4: Consulta compleja que requiere múltiples herramientas
    print("📌 TEST 4: Análisis completo (múltiples herramientas)")
    run_agent(
        "Analyze ventas.csv completely: tell me about the dataset structure, "
        "calculate price statistics, and create a distribution plot"
    )

    print("\n")
    print("=" * 80)
    print("✅ DEMO COMPLETADA")
    print("=" * 80)
