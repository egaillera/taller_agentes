"""
Script para generar un dataset de ejemplo para el workshop de agentes AI.

Este script crea un archivo CSV con datos de ventas ficticios que incluye:
- 100 filas de datos
- Productos, precios, cantidades, categorías y fechas
- Distribución realista de datos para análisis

Autor: Workshop AI Agents
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generar_dataset_ventas():
    """
    Genera un dataset de ventas con 100 filas y múltiples columnas.

    Columnas generadas:
    - producto: Identificador único del producto (Producto_1 a Producto_100)
    - precio: Precio del producto (distribución normal, media=50, std=15, min=10)
    - cantidad: Cantidad vendida (entre 1 y 100)
    - categoria: Categoría del producto (5 categorías diferentes)
    - fecha: Fecha de venta (100 días consecutivos desde 2024-01-01)
    """

    # Establecer semilla para reproducibilidad
    np.random.seed(42)

    print("🔧 Generando dataset de ventas...\n")

    # Generar datos para cada columna

    # 1. Productos: Producto_1, Producto_2, ..., Producto_100
    productos = [f"Producto_{i}" for i in range(1, 101)]
    print(f"✓ Generados {len(productos)} productos")

    # 2. Precios: Distribución normal centrada en 50, desviación estándar 15
    # Clipped a mínimo de 10 para evitar precios negativos
    precios = np.random.normal(loc=50, scale=15, size=100)
    precios = np.clip(precios, 10, None)  # Mínimo de 10
    precios = np.round(precios, 2)  # Redondear a 2 decimales
    print(f"✓ Generados precios (rango: {precios.min():.2f} - {precios.max():.2f})")

    # 3. Cantidades: Enteros aleatorios entre 1 y 100
    cantidades = np.random.randint(1, 101, size=100)
    print(f"✓ Generadas cantidades (rango: {cantidades.min()} - {cantidades.max()})")

    # 4. Categorías: 5 categorías diferentes seleccionadas aleatoriamente
    categorias = ['Electrónica', 'Ropa', 'Alimentos', 'Hogar', 'Deportes']
    categoria_column = np.random.choice(categorias, size=100)
    print(f"✓ Asignadas categorías: {', '.join(categorias)}")

    # 5. Fechas: 100 días consecutivos desde 2024-01-01
    fecha_inicio = datetime(2024, 1, 1)
    fechas = [fecha_inicio + timedelta(days=i) for i in range(100)]
    print(f"✓ Generadas fechas ({fechas[0].date()} a {fechas[-1].date()})")

    # Crear DataFrame
    df = pd.DataFrame({
        'producto': productos,
        'precio': precios,
        'cantidad': cantidades,
        'categoria': categoria_column,
        'fecha': fechas
    })

    # Guardar a CSV
    output_file = 'ventas.csv'
    df.to_csv(output_file, index=False)

    print(f"\n✅ Dataset creado exitosamente: {output_file}")
    print(f"\n📊 Resumen del dataset:")
    print(f"   - Filas: {len(df)}")
    print(f"   - Columnas: {len(df.columns)}")
    print(f"   - Tamaño: {df.memory_usage(deep=True).sum() / 1024:.2f} KB")
    print(f"\n📈 Estadísticas de precios:")
    print(f"   - Media: ${df['precio'].mean():.2f}")
    print(f"   - Mediana: ${df['precio'].median():.2f}")
    print(f"   - Desviación estándar: ${df['precio'].std():.2f}")
    print(f"\n📦 Distribución de categorías:")
    for categoria in categorias:
        count = (df['categoria'] == categoria).sum()
        print(f"   - {categoria}: {count} productos")

    print(f"\n🎯 Primeras 5 filas del dataset:")
    print(df.head().to_string(index=False))

    return df


if __name__ == "__main__":
    generar_dataset_ventas()
