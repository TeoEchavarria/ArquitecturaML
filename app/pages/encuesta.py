import streamlit as st
import numpy as np
import json
import os
from context.arquitectura_data import PREGUNTAS_ARQUITECTURA, INTERPRETACION_DIFUSA
from utils.evaluacion_helper import procesar_respuestas, generar_interpretacion_textual

def app():
    st.title("Evaluación de Arquitectura de Software")
    st.write("Responde las siguientes preguntas para recibir una recomendación sobre la arquitectura más adecuada para tu sistema.")
    
    # Configuración de sesión para guardar respuestas
    if 'respuestas' not in st.session_state:
        st.session_state.respuestas = {}
    
    if 'pagina_actual' not in st.session_state:
        st.session_state.pagina_actual = 0
    
    if 'modo_respuesta' not in st.session_state:
        st.session_state.modo_respuesta = "binario"
    
    # Selector de modo de respuesta
    modo_opciones = {
        "binario": "Respuestas Binarias (Sí/No)",
        "difuso": "Lógica Difusa (Valor entre 0 y 1)"
    }
    
    modo = st.radio(
        "Selecciona el modo de respuesta:",
        list(modo_opciones.keys()),
        format_func=lambda x: modo_opciones[x],
        key="modo_selector"
    )
    
    if modo != st.session_state.modo_respuesta:
        st.session_state.modo_respuesta = modo
        st.session_state.respuestas = {}  # Reiniciar respuestas al cambiar el modo
    
    # Dividir las preguntas por categorías para navegación
    total_categorias = len(PREGUNTAS_ARQUITECTURA)
    
    # Mostrar navegación por categorías
    if st.session_state.pagina_actual > 0:
        if st.button("← Categoría Anterior"):
            st.session_state.pagina_actual -= 1
            st.experimental_rerun()
    
    if st.session_state.pagina_actual < total_categorias - 1:
        col1, col2 = st.columns([5, 1])
        with col2:
            if st.button("Siguiente →"):
                st.session_state.pagina_actual += 1
                st.experimental_rerun()
    
    # Mostrar la categoría actual
    categoria_actual = PREGUNTAS_ARQUITECTURA[st.session_state.pagina_actual]
    st.subheader(f"Categoría: {categoria_actual['categoria']}")
    st.write(categoria_actual['descripcion'])
    
    # Mostrar las preguntas de la categoría actual
    for pregunta in categoria_actual['preguntas']:
        st.write(f"**{pregunta['id']}. {pregunta['texto']}**")
        st.caption(pregunta['descripcion'])
        
        pregunta_id = f"{st.session_state.pagina_actual}_{pregunta['id']}"
        
        # Modo de respuesta binario
        if st.session_state.modo_respuesta == "binario":
            valor = st.radio(
                f"Respuesta para pregunta {pregunta['id']}:",
                ["No", "Sí"],
                horizontal=True,
                key=f"binario_{pregunta_id}"
            )
            # Convertir a valor numérico (0 para No, 1 para Sí)
            valor_numerico = 1.0 if valor == "Sí" else 0.0
            
        # Modo de respuesta con lógica difusa
        else:
            valor_numerico = st.slider(
                f"Valor entre 0 (No) y 1 (Sí):",
                min_value=0.0,
                max_value=1.0,
                value=0.5,
                step=0.01,
                key=f"difuso_{pregunta_id}"
            )
            
            # Mostrar la interpretación difusa
            if valor_numerico <= INTERPRETACION_DIFUSA["baja"][1]:
                st.info(f"Interpretación: Valor BAJO ({valor_numerico:.2f})")
            elif valor_numerico <= INTERPRETACION_DIFUSA["media"][1]:
                st.info(f"Interpretación: Valor MEDIO ({valor_numerico:.2f})")
            else:
                st.info(f"Interpretación: Valor ALTO ({valor_numerico:.2f})")
        
        # Guardar la respuesta
        st.session_state.respuestas[f"{pregunta['id']}"] = {
            "valor": valor_numerico,
            "peso": pregunta['peso'],
            "categoria": categoria_actual['categoria']
        }
        
        st.divider()
    
    # Botón para finalizar encuesta
    if st.session_state.pagina_actual == total_categorias - 1:
        if st.button("Finalizar Encuesta y Ver Resultados"):
            # Indicar que la encuesta está completada
            st.session_state.encuesta_completada = True
            
            # Mostrar mensaje de éxito
            st.success("¡Encuesta completada! Procesando resultados...")
            
            # Calcular y guardar los resultados utilizando el helper
            resultados = procesar_respuestas(st.session_state.respuestas)
            st.session_state.resultados_encuesta = resultados
            
            # Generar interpretación preliminar
            interpretacion = generar_interpretacion_textual(resultados)
            st.session_state.interpretacion_preliminar = interpretacion
            
            # Informar al usuario que será redirigido
            st.info("A continuación, serás redirigido al chat de asesoría...")
            
            # Cambiar a la página de chat
            st.session_state.page = "chat"
            st.experimental_rerun()

if __name__ == "__main__":
    app()
