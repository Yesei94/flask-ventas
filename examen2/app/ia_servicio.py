import requests
import os

API_KEY =  os.getenv("API_KEY")

URL = "https://openrouter.ai/api/v1/chat/completions"


# =====================================================
# FUNCION GENERAL
# =====================================================

def consultar_ia(prompt):

    try:

        response = requests.post(
            url=URL,
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "deepseek/deepseek-chat",
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            },
            timeout=20
        )

        print("STATUS:", response.status_code)
        print("RESPUESTA:", response.text)

        response.raise_for_status()

        result = response.json()

        return result["choices"][0]["message"]["content"]

    except Exception as e:
        return f"ERROR IA: {str(e)}"


# =====================================================
# ANALISIS VENTAS
# =====================================================

def analizar_ventas(data):

    prompt = f"""
    Analiza las ventas del negocio.

    Datos:
    {data}

    Dame:
    - productos más vendidos
    - recomendaciones
    - oportunidades de negocio
    """

    return consultar_ia(prompt)


# =====================================================
# ANALISIS CLIENTES
# =====================================================

def analizar_clientes(data):

    prompt = f"""
    Analiza los clientes del negocio.

    Datos:
    {data}

    Dame:
    - mejores clientes
    - clientes frecuentes
    - recomendaciones de fidelización
    """

    return consultar_ia(prompt)


# =====================================================
# ANALISIS PRODUCTOS
# =====================================================

def analizar_productos(data):

    prompt = f"""
    Analiza los productos del negocio.

    Datos:
    {data}

    Dame:
    - productos más rentables
    - productos con mayores ingresos
    - recomendaciones comerciales
    """

    return consultar_ia(prompt)