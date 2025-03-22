import streamlit as st

def app():
    st.title("Bienvenido al Asesor de Arquitectura de Software")
    
    # Banner principal
    st.image("https://cdn.pixabay.com/photo/2018/03/15/16/11/background-3228704_1280.jpg", use_column_width=True)
    
    st.markdown("""
    ## ¿Qué arquitectura es mejor para tu sistema?
    
    Este asistente te ayudará a determinar la arquitectura de software más adecuada para tu proyecto
    basándose en tus respuestas a una serie de preguntas clave.
    
    ### Cómo funciona:
    
    1. **Completa la encuesta**: Responde preguntas sobre las necesidades y características de tu sistema.
    2. **Analiza los resultados**: El sistema evaluará tus respuestas y generará una recomendación.
    3. **Consulta con el chatbot**: Profundiza en detalles específicos y aclara dudas con nuestro asistente IA.
    
    ### Arquitecturas evaluadas:
    
    - **Microservicios**: Ideal para sistemas complejos con componentes independientes
    - **Arquitectura orientada a eventos**: Perfecta para sistemas con comunicación asíncrona y desacoplada
    - **Monolítica**: Adecuada para proyectos más pequeños o con fuerte cohesión
    - **Arquitecturas híbridas**: Combinación de enfoques adaptada a necesidades específicas
    """)
    
    st.info("""
    💡 **Consejo**: Para obtener resultados más precisos, considera características como escalabilidad, autonomía, 
    eventos en tiempo real y necesidades de integración de tu sistema.
    """)
    
    # Botón para iniciar la encuesta
    if st.button("Comenzar Evaluación"):
        st.session_state.pagina_actual = 0  # Reiniciar a la primera página de la encuesta
        st.session_state.respuestas = {}   # Limpiar respuestas anteriores
        st.session_state.page = "encuesta"  # Cambiar a la página de encuesta
        st.experimental_rerun()
    
    # Espacio para información adicional
    st.markdown("---")
    st.markdown("""
    ### ¿Por qué es importante elegir la arquitectura correcta?
    
    La elección de la arquitectura afecta directamente:
    - La escalabilidad y rendimiento del sistema
    - La facilidad de mantenimiento y evolución
    - Los costos de desarrollo e infraestructura
    - La resiliencia y tolerancia a fallos
    
    Nuestra herramienta te ayuda a tomar esta decisión crucial basándose en principios probados
    de ingeniería de software y las mejores prácticas de la industria.
    """)
    
    # Footer
    st.markdown("---")
    st.caption("Asesor de Arquitectura de Software © 2023")

if __name__ == "__main__":
    app()
