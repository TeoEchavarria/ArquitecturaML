# Asesor de Arquitectura de Software

Una aplicación interactiva que te ayuda a determinar la arquitectura de software más adecuada para tu proyecto, basándose en tus respuestas a un cuestionario especializado y utilizando IA para proporcionar asesoramiento personalizado.

## Características

- **Cuestionario Interactivo**: Evaluación de necesidades mediante preguntas sobre autonomía de servicios, escalabilidad, comunicación y más.
- **Evaluación Difusa**: Opción para responder con valores difusos (entre 0 y 1) o respuestas binarias (Sí/No).
- **Chat con IA**: Consulta con un chatbot especializado para profundizar en la recomendación y responder preguntas específicas.
- **Recomendación Personalizada**: Análisis de tus respuestas para sugerir la arquitectura más adecuada entre microservicios, orientada a eventos, monolítica o híbrida.

## Instalación

1. Clona este repositorio:
   ```
   git clone https://github.com/tu-usuario/asesor-arquitectura.git
   cd asesor-arquitectura
   ```

2. Crea un entorno virtual y actívalo:
   ```
   python -m venv .venv
   source .venv/bin/activate  # En Windows: .venv\Scripts\activate
   ```

3. Instala las dependencias:
   ```
   pip install -r requirements.txt
   ```

4. Configura las variables de entorno:
   ```
   cp .env.example .env
   ```
   Edita el archivo `.env` y añade tu API key de OpenAI.

## Uso

1. Inicia la aplicación:
   ```
   streamlit run app/main.py
   ```

2. Navega a través de las siguientes secciones:
   - **Inicio**: Información general sobre la herramienta
   - **Evaluación**: Cuestionario para evaluar tu sistema
   - **Chatbot**: Consulta con IA sobre las recomendaciones

## Estructura del Proyecto

```
├── app/
│   ├── components/      # Componentes reutilizables de UI
│   ├── context/         # Datos y contexto para la aplicación
│   ├── pages/           # Páginas principales de la aplicación
│   ├── utils/           # Utilidades y helpers
│   ├── config.py        # Configuración global
│   └── main.py          # Punto de entrada de la aplicación
├── data/                # Almacenamiento de datos
├── requirements.txt     # Dependencias del proyecto
├── .env.example         # Ejemplo de variables de entorno
└── README.md            # Documentación
```

## Tecnologías Utilizadas

- **Streamlit**: Framework para la interfaz de usuario
- **OpenAI API**: Para el chatbot inteligente
- **Python**: Lenguaje principal de desarrollo
- **Lógica Difusa**: Para evaluación no binaria de respuestas

## Licencia

MIT 