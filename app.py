import streamlit as st
import os
from components.survey import render_survey
from components.chatbot import render_chatbot

# Configuración de la página
st.set_page_config(
    page_title="Chatbot con Encuesta",
    page_icon="💬",
    layout="centered"
)

# Barra lateral para configuración
with st.sidebar:
    st.title("Configuración")
    api_key = st.text_input("OpenAI API Key", type="password")
    if api_key:
        os.environ["OPENAI_API_KEY"] = api_key
        st.success("API Key guardada para esta sesión")
    else:
        st.warning("Por favor, introduce tu API Key de OpenAI")

# Estado de sesión para seguimiento del flujo
if 'survey_completed' not in st.session_state:
    st.session_state.survey_completed = False

# Verificar que hay API key antes de continuar
if not api_key:
    st.info("Por favor, introduce tu API Key de OpenAI en la barra lateral para comenzar.")
elif not st.session_state.survey_completed:
    # Renderizar la encuesta
    render_survey()
else:
    # Renderizar el chatbot
    render_chatbot() 