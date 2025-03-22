import streamlit as st
import os
from pages import inicio, encuesta, chat
from config import APP_TITLE, APP_DESCRIPTION

def main():
    # Configuración inicial de la aplicación
    st.set_page_config(
        page_title=APP_TITLE,
        page_icon="🏛️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Inicializar estado de sesión
    if 'page' not in st.session_state:
        st.session_state.page = "inicio"
    
    # Barra lateral
    with st.sidebar:
        st.title("Asesor de Arquitectura")
        st.markdown("---")
        
        # Opciones de navegación
        pages = {
            "inicio": "🏠 Inicio",
            "encuesta": "📝 Evaluación",
            "chat": "💬 Chatbot"
        }
        
        # Navegación a través de botones
        for page_id, page_name in pages.items():
            if st.button(page_name, key=f"nav_{page_id}", use_container_width=True):
                st.session_state.page = page_id
                st.experimental_rerun()
        
        st.markdown("---")
        st.caption("Desarrollado con Streamlit y OpenAI")
        
        # Información adicional
        with st.expander("ℹ️ Acerca de"):
            st.write(APP_DESCRIPTION)
            st.write("Este asistente utiliza IA para ayudarte a determinar la arquitectura de software más adecuada para tu proyecto.")
    
    # Renderizar la página actual
    if st.session_state.page == "inicio":
        inicio.app()
    elif st.session_state.page == "encuesta":
        encuesta.app()
    elif st.session_state.page == "chat":
        chat.app()

if __name__ == "__main__":
    main()
