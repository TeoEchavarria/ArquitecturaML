import streamlit as st

def render_survey():
    """
    Renderiza el formulario de encuesta y almacena datos en session_state
    """
    st.title("Bienvenido al Chatbot")
    st.subheader("Por favor, responde estas preguntas antes de comenzar:")
    
    with st.form("survey_form"):
        # Datos básicos
        name = st.text_input("Nombre:")
        age = st.number_input("Edad:", min_value=1, max_value=120, value=25)
        
        # Preferencias
        experience = st.selectbox(
            "¿Qué nivel de experiencia tienes con chatbots?",
            options=["Principiante", "Intermedio", "Avanzado"]
        )
        
        interests = st.multiselect(
            "¿Qué temas te interesan?",
            options=["Tecnología", "Ciencia", "Arte", "Deportes", "Música", "Otros"]
        )
        
        feedback = st.text_area("¿Qué esperas de esta conversación con el chatbot?")
        
        # Botón para enviar
        submitted = st.form_submit_button("Comenzar Conversación")
        
        if submitted:
            if name and interests:  # Validación básica
                # Almacenar datos solo en session_state
                survey_data = {
                    "name": name,
                    "age": age,
                    "experience": experience,
                    "interests": interests,
                    "feedback": feedback
                }
                
                # Actualizar estado
                st.session_state.survey_data = survey_data
                st.session_state.survey_completed = True
                st.session_state.user_name = name
                
                st.success("¡Gracias por completar la encuesta! Ahora puedes comenzar a chatear.")
                st.balloons()
                st.experimental_rerun()
            else:
                st.error("Por favor completa al menos tu nombre y selecciona algún tema de interés.") 