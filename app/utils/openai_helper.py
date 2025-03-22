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
            # Verificar si hay arquitecturas con puntuaciones cercanas
            if context.get("tiene_arquitecturas_cercanas", False):
                arq_principal = context.get("arquitectura_principal", "")
                arq_cercanas = context.get("arquitecturas_cercanas", [])
                
                # Agregar instrucciones específicas para el caso de arquitecturas cercanas
                hybrid_prompt = f"""
                IMPORTANTE: En este caso, el usuario tiene varias arquitecturas con puntuaciones muy cercanas:
                - Arquitectura principal: {arq_principal}
                - Arquitecturas cercanas: {', '.join(arq_cercanas)}
                
                {context.get('guia_hibrida', '')}
                
                Cuando respondas, considera estos aspectos híbridos y profundiza en:
                1. Cómo pueden combinarse efectivamente estas arquitecturas
                2. Qué elementos de cada una deberían priorizarse
                3. Estrategias de implementación incremental
                4. Patrones arquitectónicos que faciliten la integración
                5. Ejemplos concretos de sistemas que utilizan enfoques híbridos similares
                
                Sé específico con ejemplos y recomendaciones concretas, no solo teóricas.
                """
                
                messages.append({"role": "system", "content": hybrid_prompt})
            
            # Agregar resultados de la encuesta como contexto
            if "resultados_encuesta" in context:
                resultados = context["resultados_encuesta"]
                # Convertir solo lo necesario a texto para evitar mensajes demasiado largos
                puntuaciones_globales = resultados.get("puntuaciones_globales", {})
                recomendacion = resultados.get("recomendacion", {})
                
                categorias = [cat for cat in resultados.keys() if cat not in ["puntuaciones_globales", "recomendacion"]]
                promedios_categorias = {cat: resultados[cat].get("promedio", 0) for cat in categorias}
                
                # Crear un resumen más compacto de los resultados
                resultados_resumidos = {
                    "puntuaciones_globales": puntuaciones_globales,
                    "recomendacion": recomendacion,
                    "promedios_categorias": promedios_categorias
                }
                
                resultados_texto = json.dumps(resultados_resumidos, indent=2, ensure_ascii=False)
                context_message = f"""
                Información resumida de la encuesta del usuario:
                {resultados_texto}
                
                Interpretación preliminar: {context.get('interpretacion_preliminar', 'No disponible')}
                """
                messages.append({"role": "system", "content": context_message})
            
            # Cargar contextos específicos por tipo de arquitectura
            if "resultados_encuesta" in context and "recomendacion" in context["resultados_encuesta"]:
                recomendacion = context["resultados_encuesta"]["recomendacion"]
                tipo_recomendacion = recomendacion.get("tipo", "")
                
                # Si hay arquitecturas cercanas, cargar contextos específicos para todas ellas
                if context.get("tiene_arquitecturas_cercanas", False):
                    # Cargar contexto de la arquitectura principal
                    contexto_principal = cargar_contexto_arquitectura(tipo_recomendacion)
                    if contexto_principal:
                        messages.append({"role": "system", "content": contexto_principal})
                    
                    # Cargar contexto de las arquitecturas cercanas
                    for arq_cercana in context.get("arquitecturas_cercanas", []):
                        contexto_cercana = cargar_contexto_arquitectura(arq_cercana)
                        if contexto_cercana:
                            messages.append({"role": "system", "content": contexto_cercana})
                else:
                    # Solo cargar el contexto de la arquitectura recomendada
                    contexto_arquitectura = cargar_contexto_arquitectura(tipo_recomendacion)
                    if contexto_arquitectura:
                        messages.append({"role": "system", "content": contexto_arquitectura})
            
            # Agregar historial de chat si está disponible
            if "historial_chat" in context:
                for msg in context["historial_chat"]:
                    messages.append(msg)
        
        # Agregar el mensaje actual del usuario
        messages.append({"role": "user", "content": user_message})
        
        # Obtener respuesta de OpenAI
        response = openai.ChatCompletion.create(
            model=os.getenv("OPENAI_MODEL"),
            messages=messages,
            temperature=0.7,
            max_tokens=1000
        )
        
        return response.choices[0].message.content
    
    except Exception as e:
        print(f"Error al comunicarse con OpenAI: {e}")
        return f"Lo siento, ha ocurrido un error al procesar tu solicitud. Detalles: {str(e)}"

def cargar_contexto_arquitectura(tipo_arquitectura):
    """
    Carga el contexto específico para un tipo de arquitectura desde un archivo JSON.
    
    Args:
        tipo_arquitectura (str): Tipo de arquitectura (microservicios, eventos, monolitico, hibrido)
        
    Returns:
        str: Contenido del contexto o None si no se encuentra
    """
    try:
        # Mapear el tipo de arquitectura al nombre del archivo
        archivos_contexto = {
            "microservicios": "contexto_microservicios.json",
            "eventos": "contexto_eventos.json",
            "monolitico": "contexto_monolitico.json",
            "hibrido": "contexto_hibrido.json"
        }
        
        archivo = archivos_contexto.get(tipo_arquitectura)
        if not archivo:
            return None
        
        # Construir ruta al archivo de contexto (dentro de la carpeta data)
        ruta_archivo = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "data",
            archivo
        )
        
        # Verificar si el archivo existe
        if not os.path.exists(ruta_archivo):
            print(f"Archivo de contexto {ruta_archivo} no encontrado")
            return None
        
        # Cargar el contenido del archivo
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            datos = json.load(f)
            
        # El archivo debe contener un campo 'contexto' con el texto
        if 'contexto' in datos:
            return datos['contexto']
        else:
            print(f"El archivo {archivo} no contiene un campo 'contexto'")
            return None
            
    except Exception as e:
        print(f"Error al cargar el contexto de arquitectura: {e}")
        return None