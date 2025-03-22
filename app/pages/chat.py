import streamlit as st
import json
import os
from utils.openai_helper import get_openai_response

def app():
    st.title("Chat de Asesoría Arquitectónica")
    
    # Verificar si la encuesta fue completada
    if 'encuesta_completada' not in st.session_state or not st.session_state.encuesta_completada:
        st.warning("Por favor, completa la encuesta primero para recibir asesoría personalizada.")
        st.info("Ve a la página 'Encuesta' para comenzar la evaluación.")
        return
    
    # Mostrar resumen de resultados de la encuesta
    st.subheader("Resultados de tu Evaluación")
    
    resultados = st.session_state.resultados_encuesta
    
    # Crear un gráfico de resumen por categoría
    categorias = list(resultados.keys())
    promedios = [resultados[cat]["promedio"] for cat in categorias]
    
    # Mostrar promedios por categoría
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label=categorias[0][:20] + "...", 
            value=f"{promedios[0]:.2f}", 
            delta=f"{'+' if promedios[0] > 0.5 else ''}{(promedios[0] - 0.5):.2f}"
        )
    
    with col2:
        st.metric(
            label=categorias[1][:20] + "...", 
            value=f"{promedios[1]:.2f}", 
            delta=f"{'+' if promedios[1] > 0.5 else ''}{(promedios[1] - 0.5):.2f}"
        )
    
    with col3:
        st.metric(
            label=categorias[2][:20] + "...", 
            value=f"{promedios[2]:.2f}", 
            delta=f"{'+' if promedios[2] > 0.5 else ''}{(promedios[2] - 0.5):.2f}"
        )
    
    # Interpretación preliminar
    st.subheader("Interpretación Preliminar")
    
    if promedios[0] > 0.67:  # Microservicios
        interpretacion = "Basado en tus respuestas, tu sistema podría beneficiarse de una **arquitectura de microservicios**."
    elif promedios[2] > 0.67:  # Orientado a eventos
        interpretacion = "Basado en tus respuestas, tu sistema podría beneficiarse de una **arquitectura orientada a eventos**."
    elif all(p < 0.33 for p in promedios):  # Monolítico
        interpretacion = "Basado en tus respuestas, una **arquitectura monolítica** podría ser más adecuada para tu sistema."
    else:
        interpretacion = "Basado en tus respuestas, podrías considerar una **arquitectura híbrida** que combine diferentes enfoques."
    
    st.write(interpretacion)
    
    # Sección de chat
    st.subheader("Consulta con nuestro Asesor de Arquitectura")
    
    # Inicializar historial de chat si no existe
    if 'messages' not in st.session_state:
        # Mensaje inicial basado en la interpretación
        st.session_state.messages = [
            {"role": "assistant", "content": f"{interpretacion} ¿Tienes alguna pregunta específica sobre esta recomendación o quieres más detalles sobre cómo implementar esta arquitectura?"}
        ]
    
    # Mostrar mensajes previos
    for message in st.session_state.messages:
        avatar = "🧑‍💻" if message["role"] == "user" else "🤖"
        with st.chat_message(message["role"], avatar=avatar):
            st.write(message["content"])
    
    # Entrada de nuevo mensaje
    if prompt := st.chat_input("Escribe tu pregunta sobre arquitectura..."):
        # Agregar mensaje del usuario al historial
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Mostrar mensaje del usuario
        with st.chat_message("user", avatar="🧑‍💻"):
            st.write(prompt)
        
        # Preparar contexto para la API de OpenAI
        context = {
            "resultados_encuesta": resultados,
            "interpretacion_preliminar": interpretacion,
            "historial_chat": st.session_state.messages[:-1]  # Todo el historial excepto el último mensaje
        }
        
        # Obtener respuesta del modelo
        response = get_openai_response(prompt, context)
        
        # Agregar respuesta del asistente al historial
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Mostrar respuesta del asistente
        with st.chat_message("assistant", avatar="🤖"):
            st.write(response)

if __name__ == "__main__":
    app()
