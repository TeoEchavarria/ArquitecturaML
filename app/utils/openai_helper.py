import os
import json
import openai
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configurar la API key de OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_openai_response(user_message, context=None):
    """
    Obtiene una respuesta de OpenAI basada en el mensaje del usuario y el contexto.
    
    Args:
        user_message (str): El mensaje del usuario
        context (dict, optional): Contexto adicional para la consulta. 
            Puede incluir resultados de la encuesta e historial de chat.
    
    Returns:
        str: La respuesta generada por OpenAI
    """
    try:
        # Verificar que la API key está configurada
        if not openai.api_key:
            return "Error: No se ha configurado la API key de OpenAI. Por favor, configura la variable de entorno OPENAI_API_KEY."
        
        # Construir el sistema de mensajes
        system_prompt = """
        Eres un asistente experto en arquitecturas de software. Tu tarea es ayudar a los usuarios a elegir
        la arquitectura más adecuada para sus proyectos basándose en sus respuestas a un cuestionario de evaluación.
        
        Las principales arquitecturas que puedes recomendar son:
        1. Microservicios: Sistemas distribuidos con servicios independientes y autónomos.
        2. Arquitectura orientada a eventos: Sistemas basados en la comunicación por eventos y desacoplamiento.
        3. Arquitectura monolítica: Un solo sistema integrado con todos los componentes juntos.
        4. Arquitecturas híbridas: Combinación de enfoques según las necesidades específicas.
        
        Para cada recomendación, debes explicar:
        - Por qué es adecuada para el caso específico
        - Ventajas y desventajas
        - Consideraciones de implementación
        - Posibles tecnologías a utilizar
        
        Basado en los resultados de la encuesta del usuario, personaliza tus respuestas.
        """
        
        messages = [{"role": "system", "content": system_prompt}]
        
        # Agregar contexto si está disponible
        if context:
            # Agregar resultados de la encuesta como contexto
            if "resultados_encuesta" in context:
                resultados = context["resultados_encuesta"]
                resultados_texto = json.dumps(resultados, indent=2, ensure_ascii=False)
                context_message = f"""
                Información de la encuesta del usuario:
                {resultados_texto}
                
                Interpretación preliminar: {context.get('interpretacion_preliminar', 'No disponible')}
                """
                messages.append({"role": "system", "content": context_message})
            
            # Agregar historial de chat si está disponible
            if "historial_chat" in context:
                for msg in context["historial_chat"]:
                    messages.append(msg)
        
        # Agregar el mensaje actual del usuario
        messages.append({"role": "user", "content": user_message})
        
        # Obtener respuesta de OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Puedes usar 'gpt-3.5-turbo' como alternativa
            messages=messages,
            temperature=0.7,
            max_tokens=1000
        )
        
        return response.choices[0].message.content
    
    except Exception as e:
        print(f"Error al comunicarse con OpenAI: {e}")
        return f"Lo siento, ha ocurrido un error al procesar tu solicitud. Detalles: {str(e)}"

# Función de prueba
if __name__ == "__main__":
    test_message = "¿Qué ventajas tiene una arquitectura de microservicios?"
    print(get_openai_response(test_message))
