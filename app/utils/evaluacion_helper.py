"""
Utilidades para evaluar resultados de la encuesta de arquitectura.
Este módulo se encarga de calcular los puntajes y determinar la arquitectura más adecuada.
"""
import numpy as np
from context.arquitectura_data import PREGUNTAS_ARQUITECTURA, INTERPRETACION_DIFUSA
from config import UMBRAL_BAJO, UMBRAL_MEDIO, UMBRAL_ALTO, PESOS_CATEGORIAS, FRASES_INTERPRETACION

def procesar_respuestas(respuestas):
    """
    Procesa las respuestas de la encuesta y calcula los resultados por categoría.
    
    Args:
        respuestas (dict): Diccionario con las respuestas de la encuesta
            
    Returns:
        dict: Resultados procesados con puntuaciones por categoría
    """
    resultados = {}
    
    # Agrupar por categorías
    for categoria in PREGUNTAS_ARQUITECTURA:
        nombre_categoria = categoria['categoria']
        resultados[nombre_categoria] = {
            "puntuacion_ponderada": 0,
            "total_preguntas": 0,
            "respuestas": []
        }
    
    # Procesar las respuestas
    for id_pregunta, respuesta in respuestas.items():
        categoria = respuesta['categoria']
        valor = respuesta['valor']
        peso = respuesta['peso']
        
        resultados[categoria]["puntuacion_ponderada"] += valor * peso
        resultados[categoria]["total_preguntas"] += 1
        resultados[categoria]["respuestas"].append({
            "id": id_pregunta,
            "valor": valor,
            "peso": peso
        })
    
    # Calcular el promedio ponderado para cada categoría
    for categoria in resultados:
        if resultados[categoria]["total_preguntas"] > 0:
            resultados[categoria]["promedio"] = resultados[categoria]["puntuacion_ponderada"] / resultados[categoria]["total_preguntas"]
        else:
            resultados[categoria]["promedio"] = 0
    
    # Calcular puntuaciones globales
    calcular_puntuaciones_globales(resultados)
    
    return resultados

def calcular_puntuaciones_globales(resultados):
    """
    Calcula puntuaciones globales para cada tipo de arquitectura basado en los resultados por categoría.
    
    Args:
        resultados (dict): Resultados de la encuesta por categoría
    
    Returns:
        dict: El mismo diccionario resultados con las puntuaciones globales añadidas
    """
    # Extraer los promedios por categoría
    promedios = {cat: resultados[cat]["promedio"] for cat in resultados}
    
    # Extraer las categorías para facilitar el acceso
    cat_microservicios = "División y Autonomía de Servicios"
    cat_global = "Disponibilidad, Integración y Escalabilidad Global"
    cat_eventos = "Arquitectura Orientada a Eventos"
    
    # Calcular puntuación para microservicios (ponderada por las categorías relevantes)
    # Usamos principalmente la categoría de autonomía de servicios y la global
    peso_ms_autonomia = PESOS_CATEGORIAS[cat_microservicios]
    peso_ms_global = PESOS_CATEGORIAS[cat_global] * 0.7  # Damos menos peso a la parte global
    
    puntuacion_microservicios = (
        promedios[cat_microservicios] * peso_ms_autonomia + 
        promedios[cat_global] * peso_ms_global
    ) / (peso_ms_autonomia + peso_ms_global)
    
    # Calcular puntuación para arquitectura orientada a eventos
    # Usamos principalmente la categoría de eventos y parte de la global
    peso_ev_eventos = PESOS_CATEGORIAS[cat_eventos]
    peso_ev_global = PESOS_CATEGORIAS[cat_global] * 0.3  # Damos menos peso a la parte global
    
    puntuacion_eventos = (
        promedios[cat_eventos] * peso_ev_eventos + 
        promedios[cat_global] * peso_ev_global
    ) / (peso_ev_eventos + peso_ev_global)
    
    # Calcular puntuación para monolítico (inverso de microservicios)
    # Cuando la puntuación de microservicios es baja, monolítico es alto
    puntuacion_monolitico = 1 - puntuacion_microservicios
    
    # Calcular puntuación híbrida (promedio entre microservicios y eventos)
    puntuacion_hibrida = (puntuacion_microservicios + puntuacion_eventos) / 2
    
    # Guardar resultados globales
    resultados["puntuaciones_globales"] = {
        "microservicios": puntuacion_microservicios,
        "eventos": puntuacion_eventos,
        "monolitico": puntuacion_monolitico,
        "hibrido": puntuacion_hibrida
    }
    
    # Determinar la recomendación final
    resultados["recomendacion"] = determinar_recomendacion(resultados["puntuaciones_globales"])
    
    return resultados

def determinar_recomendacion(puntuaciones):
    """
    Determina la recomendación de arquitectura basada en las puntuaciones.
    
    Args:
        puntuaciones (dict): Puntuaciones globales para cada tipo de arquitectura
    
    Returns:
        dict: Información sobre la recomendación
    """
    # Obtener la arquitectura con mayor puntuación
    arquitecturas = list(puntuaciones.keys())
    max_arquitectura = max(arquitecturas, key=lambda x: puntuaciones[x])
    
    # Determinar si hay una diferencia significativa o si las puntuaciones están cerca
    max_puntuacion = puntuaciones[max_arquitectura]
    cercanas = []
    
    for arq in arquitecturas:
        if arq != max_arquitectura and (max_puntuacion - puntuaciones[arq]) < 0.15:
            cercanas.append(arq)
    
    # Generar la recomendación
    if max_arquitectura == "microservicios":
        tipo_recomendacion = "microservicios"
        descripcion = "Arquitectura de Microservicios"
        mensaje = FRASES_INTERPRETACION["microservicios"][0]
    elif max_arquitectura == "eventos":
        tipo_recomendacion = "eventos"
        descripcion = "Arquitectura Orientada a Eventos"
        mensaje = FRASES_INTERPRETACION["eventos"][0]
    elif max_arquitectura == "monolitico":
        tipo_recomendacion = "monolitico"
        descripcion = "Arquitectura Monolítica / N-Tier"
        mensaje = FRASES_INTERPRETACION["monolitico"][0]
    else:  # híbrida
        tipo_recomendacion = "hibrido"
        descripcion = "Arquitectura Híbrida"
        mensaje = FRASES_INTERPRETACION["hibrido"][0]
    
    # Si hay arquitecturas con puntuaciones cercanas, recomendar enfoque híbrido
    if cercanas:
        arquitecturas_cercanas = [obtener_nombre_arquitectura(arq) for arq in cercanas]
        tipo_recomendacion = "hibrido"
        descripcion = f"Arquitectura Híbrida (combinando {descripcion} con {', '.join(arquitecturas_cercanas)})"
        mensaje = FRASES_INTERPRETACION["hibrido"][0]
    
    return {
        "tipo": tipo_recomendacion,
        "descripcion": descripcion,
        "mensaje": mensaje,
        "puntuacion": max_puntuacion,
        "cercanas": cercanas
    }

def obtener_nombre_arquitectura(codigo):
    """Convierte el código de arquitectura a nombre legible"""
    nombres = {
        "microservicios": "Microservicios",
        "eventos": "Orientada a Eventos",
        "monolitico": "Monolítica",
        "hibrido": "Híbrida"
    }
    return nombres.get(codigo, codigo)

def generar_interpretacion_textual(resultados):
    """
    Genera una interpretación textual de los resultados de la encuesta.
    
    Args:
        resultados (dict): Resultados procesados de la encuesta
    
    Returns:
        str: Texto de interpretación
    """
    puntuaciones = resultados["puntuaciones_globales"]
    recomendacion = resultados["recomendacion"]
    
    # Obtener los promedios por categoría
    promedios = [resultados[cat]["promedio"] for cat in resultados if cat not in ["puntuaciones_globales", "recomendacion"]]
    
    # Generar mensaje base según la recomendación principal
    if recomendacion["tipo"] == "microservicios":
        mensaje = "Basado en tus respuestas, tu sistema podría beneficiarse de una **arquitectura de microservicios**."
    elif recomendacion["tipo"] == "eventos":
        mensaje = "Basado en tus respuestas, tu sistema podría beneficiarse de una **arquitectura orientada a eventos**."
    elif recomendacion["tipo"] == "monolitico" or all(p < UMBRAL_BAJO for p in promedios):
        mensaje = "Basado en tus respuestas, una **arquitectura monolítica** podría ser más adecuada para tu sistema."
    else:
        mensaje = "Basado en tus respuestas, podrías considerar una **arquitectura híbrida** que combine diferentes enfoques."
    
    # Si la puntuación no es muy alta, agregar matiz
    if recomendacion["puntuacion"] < 0.75:
        mensaje += " Sin embargo, la puntuación no es muy alta, lo que sugiere que podrías considerar también enfoques alternativos."
    
    return mensaje 