import openai
import os

def get_chatbot_response(messages):
    """
    Genera una respuesta del chatbot usando la API de OpenAI,
    utilizando el historial completo de mensajes para mantener contexto
    
    Args:
        messages (list): Lista de mensajes previos incluyendo el sistema y conversación
    
    Returns:
        str: Respuesta del chatbot
    """
    # Configura tu API key desde variables de entorno
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    
    try:
        # Llamada a la API de OpenAI con todo el historial de mensajes
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",  # Puedes ajustar el modelo según tus necesidades
            messages=messages,
            max_tokens=150,
            temperature=0.7
        )
        
        # Extraer y devolver la respuesta
        return response.choices[0].message.content
    
    except Exception as e:
        # Manejar errores de la API
        print(f"Error al llamar a la API de OpenAI: {str(e)}")
        return "Lo siento, estoy teniendo problemas para responder en este momento. ¿Podrías intentarlo de nuevo?" 