import streamlit as st
from utils.chatbot_handler import get_chatbot_response

def render_chatbot():
    """
    Renderiza la interfaz del chatbot y maneja la interacción
    """
    st.title(f"Chatbot 🤖")
    
    # Personalización según datos de la encuesta
    if 'user_name' in st.session_state:
        st.markdown(f"Hola **{st.session_state.user_name}**, ¿en qué puedo ayudarte hoy?")
    
    # Inicializar historial de chat si no existe
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
        
    # Inicializar mensajes para OpenAI si no existe
    if 'openai_messages' not in st.session_state:
        # Crear mensaje inicial del sistema
        survey_data = st.session_state.get('survey_data', {})
        system_message = create_system_message(survey_data)
        st.session_state.openai_messages = [
            {"role": "system", "content": system_message}
        ]
    
    # Mostrar historial de chat
    for message in st.session_state.chat_history:
        if message['role'] == 'user':
            st.chat_message('user').write(message['content'])
        else:
            st.chat_message('assistant').write(message['content'])
    
    # Input para nuevo mensaje
    user_input = st.chat_input("Escribe un mensaje...")
    
    if user_input:
        # Agregar mensaje del usuario al historial visible
        st.session_state.chat_history.append({
            'role': 'user',
            'content': user_input
        })
        
        # Agregar mensaje del usuario al contexto de OpenAI
        st.session_state.openai_messages.append({
            'role': 'user',
            'content': user_input
        })
        
        # Mostrar mensaje del usuario (el más reciente)
        st.chat_message('user').write(user_input)
        
        # Obtener respuesta del chatbot
        with st.spinner('Pensando...'):
            bot_response = get_chatbot_response(
                st.session_state.openai_messages
            )
        
        # Agregar respuesta del chatbot al historial visible
        st.session_state.chat_history.append({
            'role': 'assistant',
            'content': bot_response
        })
        
        # Agregar respuesta del chatbot al contexto de OpenAI
        st.session_state.openai_messages.append({
            'role': 'assistant',
            'content': bot_response
        })
        
        # Mostrar respuesta del chatbot
        st.chat_message('assistant').write(bot_response)
    
    # Botón para reiniciar la conversación
    if st.button("Reiniciar conversación"):
        # Reiniciar historial visible
        st.session_state.chat_history = []
        
        # Reiniciar contexto de OpenAI pero mantener el mensaje del sistema
        survey_data = st.session_state.get('survey_data', {})
        system_message = create_system_message(survey_data)
        st.session_state.openai_messages = [
            {"role": "system", "content": system_message}
        ]
        
        st.experimental_rerun()

def create_system_message(survey_data):
    """
    Crea un mensaje del sistema personalizado basado en los datos de la encuesta
    """
    system_message = "Eres un asistente amigable y útil."
    
    if survey_data:
        name = survey_data.get("name", "")
        interests = survey_data.get("interests", [])
        experience = survey_data.get("experience", "")
        
        # Personalizar el mensaje del sistema con los datos de la encuesta
        if name:
            system_message = f"Eres un asistente amigable y útil. Estás hablando con {name}. "
        
        if interests:
            system_message += f"Sus intereses incluyen: {', '.join(interests)}. "
            
        if experience:
            system_message += f"Su nivel de experiencia con chatbots es: {experience}. "
            
        system_message += "Adapta tus respuestas considerando esta información."
    
    return system_message 