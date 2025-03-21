# Chatbot con Encuesta

Un proyecto sencillo de chatbot usando Streamlit y OpenAI que incluye una encuesta inicial para personalizar las respuestas del asistente.

## Características

- Encuesta inicial para recopilar información del usuario
- Integración con la API de OpenAI
- Interfaz de usuario intuitiva con Streamlit
- Personalización de respuestas basada en datos de la encuesta
- Mantenimiento de contexto de conversación completo

## Requisitos

- Python 3.7+
- API key de OpenAI

## Instalación

1. Clona este repositorio:
```
git clone <url-del-repositorio>
cd chatbot-encuesta
```

2. Instala las dependencias:
```
pip install -r requirements.txt
```

## Uso

1. Ejecuta la aplicación:
```
streamlit run app.py
```

2. Abre tu navegador y accede a `http://localhost:8501`

3. Introduce tu API key de OpenAI en la barra lateral

4. Completa la encuesta inicial

5. ¡Comienza a chatear!

## Estructura del Proyecto

```
.
├── app.py                  # Punto de entrada principal
├── components/             # Componentes de la interfaz
│   ├── __init__.py
│   ├── chatbot.py          # Componente del chatbot
│   └── survey.py           # Componente de la encuesta
├── utils/                  # Utilidades
│   ├── __init__.py
│   └── chatbot_handler.py  # Manejo de la API de OpenAI
├── requirements.txt        # Dependencias
└── README.md               # Este archivo
``` 