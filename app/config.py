"""
Archivo de configuración para la aplicación de Asesoría Arquitectónica.
Contiene constantes y ajustes globales para toda la aplicación.
"""
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de la aplicación
APP_TITLE = "Asesor de Arquitectura de Software"
APP_DESCRIPTION = """
Una herramienta para ayudarte a determinar la arquitectura de software
más adecuada para tu proyecto, basándose en las características y
requerimientos específicos de tu sistema.
"""

# Configuración de OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")  # Modelo por defecto

# Umbrales para interpretación difusa
UMBRAL_BAJO = 0.33
UMBRAL_MEDIO = 0.66
UMBRAL_ALTO = 0.67

# Pesos de las categorías para el cálculo final
PESOS_CATEGORIAS = {
    "División y Autonomía de Servicios": 0.4,
    "Disponibilidad, Integración y Escalabilidad Global": 0.35,
    "Arquitectura Orientada a Eventos": 0.25
}

# Rutas de archivos
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
os.makedirs(DATA_DIR, exist_ok=True)

# Archivo para guardar resultados de encuestas
RESULTADOS_FILE = os.path.join(DATA_DIR, "resultados.json")

# Frases de interpretación de resultados
FRASES_INTERPRETACION = {
    "microservicios": [
        "Tu sistema parece ideal para una arquitectura de microservicios.",
        "La modularidad y escalabilidad independiente serían beneficiosas para tu caso.",
        "Considera implementar una arquitectura distribuida con servicios autónomos."
    ],
    "eventos": [
        "Un enfoque orientado a eventos sería muy adecuado para tu sistema.",
        "La comunicación asíncrona y el desacoplamiento ofrecerían grandes ventajas.",
        "Te recomendamos explorar patrones como Event Sourcing y CQRS."
    ],
    "monolitico": [
        "Una arquitectura monolítica sería más adecuada para tu caso.",
        "La simplicidad y cohesión del monolito ofrecen ventajas para tu escenario.",
        "Considera un diseño modular dentro de tu aplicación monolítica."
    ],
    "hibrido": [
        "Un enfoque híbrido podría ser lo más adecuado para tu sistema.",
        "Podrías beneficiarte de combinar aspectos de microservicios con un núcleo monolítico.",
        "Considera una estrategia de migración gradual hacia una arquitectura más distribuida."
    ]
}
