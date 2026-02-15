"""
CSV Data Analyst Agent - Solución Completa

Este es el código completo y funcional del agente que puede analizar datasets
CSV mediante consultas en lenguaje natural.

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
# SYSTEM PROMPT COMPLETO
# ============================================

SYSTEM_PROMPT = """
You are a data analysis assistant expert in analyzing CSV datasets.

Your capabilities:
- Load and describe CSV files to understand their structure
- Calculate descriptive statistics for numeric columns
- Create visualizations (histograms) to show data distributions

When the user asks you to analyze data:
1. First load and describe the dataset to understand its structure
2. Then use appropriate tools to answer the specific question
3. If creating visualizations, inform the user where the plot was saved
4. Always provide clear interpretations of the results

Always be clear, concise, and provide actionable insights.
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
    try:
        # Cargar el archivo CSV
        df = pd.read_csv(filepath)

        # Obtener dimensiones
        filas, columnas = df.shape

        # Construir información del dataset
        info = f"📊 INFORMACIÓN DEL DATASET: {filepath}\n\n"
        info += f"📏 Dimensiones: {filas} filas x {columnas} columnas\n\n"

        # Nombres de columnas
        info += f"📋 Columnas:\n"
        for col in df.columns:
            info += f"   - {col}\n"

        # Tipos de datos
        info += f"\n🔤 Tipos de datos:\n"
        for col, dtype in df.dtypes.items():
            info += f"   - {col}: {dtype}\n"

        # Primeras filas
        info += f"\n🔍 Primeras 3 filas:\n"
        info += df.head(3).to_string(index=False)

        return info

    except FileNotFoundError:
        return f"❌ Error: El archivo '{filepath}' no existe. Por favor verifica la ruta."

    except pd.errors.EmptyDataError:
        return f"❌ Error: El archivo '{filepath}' está vacío."

    except pd.errors.ParserError:
        return f"❌ Error: No se pudo parsear '{filepath}'. Asegúrate de que sea un CSV válido."

    except Exception as e:
        return f"❌ Error inesperado al cargar el archivo: {str(e)}"


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
    try:
        # Cargar el archivo CSV
        df = pd.read_csv(filepath)

        # Verificar que la columna existe
        if column not in df.columns:
            available_columns = ", ".join(df.columns)
            return (
                f"❌ Error: La columna '{column}' no existe en el dataset.\n"
                f"Columnas disponibles: {available_columns}"
            )

        # Verificar que la columna es numérica
        if not pd.api.types.is_numeric_dtype(df[column]):
            return (
                f"❌ Error: La columna '{column}' no es numérica (tipo: {df[column].dtype}).\n"
                f"Las estadísticas solo se pueden calcular para columnas numéricas."
            )

        # Calcular estadísticas usando describe()
        stats = df[column].describe()

        # Formatear resultados
        result = f"📊 ESTADÍSTICAS DESCRIPTIVAS: '{column}'\n\n"
        result += f"📈 Medidas de tendencia central:\n"
        result += f"   - Media (promedio): {stats['mean']:.2f}\n"
        result += f"   - Mediana (50%): {stats['50%']:.2f}\n\n"

        result += f"📏 Medidas de dispersión:\n"
        result += f"   - Desviación estándar: {stats['std']:.2f}\n"
        result += f"   - Mínimo: {stats['min']:.2f}\n"
        result += f"   - Máximo: {stats['max']:.2f}\n"
        result += f"   - Rango: {stats['max'] - stats['min']:.2f}\n\n"

        result += f"📊 Cuartiles:\n"
        result += f"   - Q1 (25%): {stats['25%']:.2f}\n"
        result += f"   - Q2 (50%, mediana): {stats['50%']:.2f}\n"
        result += f"   - Q3 (75%): {stats['75%']:.2f}\n"
        result += f"   - IQR (rango intercuartil): {stats['75%'] - stats['25%']:.2f}\n\n"

        result += f"🔢 Conteo:\n"
        result += f"   - Total de valores: {int(stats['count'])}\n"

        return result

    except FileNotFoundError:
        return f"❌ Error: El archivo '{filepath}' no existe."

    except Exception as e:
        return f"❌ Error al calcular estadísticas: {str(e)}"


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
    try:
        # Cargar el archivo CSV
        df = pd.read_csv(filepath)

        # Verificar que la columna existe
        if column not in df.columns:
            available_columns = ", ".join(df.columns)
            return (
                f"❌ Error: La columna '{column}' no existe en el dataset.\n"
                f"Columnas disponibles: {available_columns}"
            )

        # Verificar que la columna es numérica
        if not pd.api.types.is_numeric_dtype(df[column]):
            return (
                f"❌ Error: La columna '{column}' no es numérica (tipo: {df[column].dtype}).\n"
                f"Los histogramas solo se pueden crear para columnas numéricas."
            )

        # Crear la figura
        plt.figure(figsize=(10, 6))

        # Crear el histograma
        plt.hist(df[column], bins=20, edgecolor='black', alpha=0.7, color='skyblue')

        # Configurar el gráfico
        plt.title(f'Distribución de {column}', fontsize=16, fontweight='bold')
        plt.xlabel(column, fontsize=12)
        plt.ylabel('Frecuencia', fontsize=12)
        plt.grid(True, alpha=0.3, linestyle='--')

        # Añadir línea vertical para la media
        mean_value = df[column].mean()
        plt.axvline(mean_value, color='red', linestyle='--', linewidth=2, label=f'Media: {mean_value:.2f}')
        plt.legend()

        # Ajustar layout
        plt.tight_layout()

        # Guardar la figura
        output_path = PLOTS_DIR / f'{column}_histogram.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight')

        # Cerrar la figura para liberar memoria
        plt.close()

        return (
            f"✅ Histograma creado exitosamente!\n\n"
            f"📁 Guardado en: {output_path.absolute()}\n"
            f"📊 Columna: {column}\n"
            f"📈 Media: {mean_value:.2f}\n"
            f"🔢 Valores graficados: {len(df[column])}"
        )

    except FileNotFoundError:
        return f"❌ Error: El archivo '{filepath}' no existe."

    except Exception as e:
        return f"❌ Error al crear el histograma: {str(e)}"


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
