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

import sys
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
    Ejecuta el agente con una consulta y muestra únicamente la respuesta final.

    Args:
        query: Pregunta o solicitud del usuario en lenguaje natural

    Returns:
        Respuesta final del agente
    """
    try:
        result = agent.invoke({"messages": [("user", query)]})
        messages = result.get("messages", [])
        if messages:
            raw = messages[-1].content
            if isinstance(raw, list):
                response = " ".join(
                    part.get("text", "") if isinstance(part, dict) else str(part)
                    for part in raw
                ).strip()
            else:
                response = raw
            print(response)
            return response
        return "No se pudo obtener una respuesta del agente"
    except Exception as e:
        error_msg = f"❌ Error al ejecutar el agente: {str(e)}"
        print(error_msg)
        return error_msg


def run_agent_verbose(query: str) -> str:
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
            # LangGraph usa "model" o "agent" como clave según la versión
            agent_key = "model" if "model" in step else "agent" if "agent" in step else None

            if agent_key:
                messages = step[agent_key]["messages"]

                for message in messages:
                    # Extraer contenido de texto (puede ser str o lista de partes)
                    text_content = ""
                    if hasattr(message, "content") and message.content:
                        if isinstance(message.content, str):
                            text_content = message.content
                        elif isinstance(message.content, list):
                            # Gemini devuelve una lista de partes
                            text_content = " ".join(
                                part.get("text", "") if isinstance(part, dict) else str(part)
                                for part in message.content
                            ).strip()

                    # Mostrar el razonamiento del agente
                    if text_content:
                        print(f"💭 RAZONAMIENTO (Paso {step_number}):")
                        print(f"   {text_content}")
                        print()

                    # Mostrar llamadas a herramientas
                    tool_calls = getattr(message, "tool_calls", None) or []
                    # Algunos modelos usan additional_kwargs para tool_calls
                    if not tool_calls and hasattr(message, "additional_kwargs"):
                        tool_calls = message.additional_kwargs.get("tool_calls", [])

                    for tc in tool_calls:
                        name = tc.get("name", tc.get("function", {}).get("name", "desconocida"))
                        args = tc.get("args", tc.get("function", {}).get("arguments", {}))
                        print(f"🔧 USANDO HERRAMIENTA: {name}")
                        print(f"   Argumentos: {args}")
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
        final_key = "model" if result and "model" in result else "agent" if result and "agent" in result else None
        if final_key:
            final_messages = result[final_key]["messages"]
            if final_messages:
                raw = final_messages[-1].content
                if isinstance(raw, list):
                    final_response = " ".join(
                        part.get("text", "") if isinstance(part, dict) else str(part)
                        for part in raw
                    ).strip()
                else:
                    final_response = raw
                if final_response:
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

def run_demo(executor=run_agent):
    """Ejecuta los 4 casos de prueba de demostración."""
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
    executor("How many rows and columns does ventas.csv have? What columns does it contain?")

    # Test 2: Estadísticas
    print("📌 TEST 2: Cálculo de estadísticas")
    executor("What is the average price and standard deviation in ventas.csv?")

    # Test 3: Visualización
    print("📌 TEST 3: Creación de visualización")
    executor("Create a histogram of the 'precio' column from ventas.csv")

    # Test 4: Consulta compleja que requiere múltiples herramientas
    print("📌 TEST 4: Análisis completo (múltiples herramientas)")
    executor(
        "Analyze ventas.csv completely: tell me about the dataset structure, "
        "calculate price statistics, and create a distribution plot"
    )

    print("\n")
    print("=" * 80)
    print("✅ DEMO COMPLETADA")
    print("=" * 80)


def interactive_mode(executor=run_agent):
    """Modo interactivo: el usuario escribe consultas para el agente."""
    print("\n")
    print("🤖 CSV DATA ANALYST AGENT - MODO INTERACTIVO")
    print("=" * 80)
    print()
    print("Escribe tu consulta para el agente y presiona ENTER.")
    print("Para salir, escribe 'salir', 'exit' o deja la línea vacía.\n")

    while True:
        try:
            query = input("📝 Tu consulta: ").strip()
        except (KeyboardInterrupt, EOFError):
            print()
            break

        if not query or query.lower() in ("salir", "exit"):
            break

        executor(query)
        print()

    print("\n" + "=" * 80)
    print("👋 ¡Hasta luego!")
    print("=" * 80)


if __name__ == "__main__":
    executor = run_agent_verbose if "--verbose" in sys.argv else run_agent
    if "--test" in sys.argv:
        run_demo(executor)
    else:
        interactive_mode(executor)
