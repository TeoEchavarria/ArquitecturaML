"""
Datos de preguntas para la evaluación de arquitectura de software.
Organización de preguntas por categorías para el chatbot de recomendación.
"""

# Estructura de preguntas para la evaluación de arquitectura
PREGUNTAS_ARQUITECTURA = [
    {
        "categoria": "División y Autonomía de Servicios",
        "descripcion": "Evalúa la capacidad del sistema para dividirse en servicios independientes",
        "preguntas": [
            {
                "id": 1,
                "texto": "¿El sistema se puede dividir en servicios autónomos sin afectar la funcionalidad global?",
                "descripcion": "Evalúa la capacidad de descomposición del sistema.",
                "peso": 0.9
            },
            {
                "id": 2,
                "texto": "¿Cada servicio tiene una lógica de negocio clara y bien definida (aplicando Bounded Context de Domain-Driven Design)?",
                "descripcion": "Permite determinar si existen límites precisos que favorecen la independencia.",
                "peso": 0.85
            },
            {
                "id": 3,
                "texto": "¿Los servicios requieren escalabilidad independiente?",
                "descripcion": "Indica si es necesario escalar ciertos módulos sin afectar al resto.",
                "peso": 0.8
            },
            {
                "id": 4,
                "texto": "¿Cada servicio puede tener su propia base de datos sin necesidad de acceso directo a las de otros?",
                "descripcion": "Evalúa la viabilidad de la persistencia descentralizada.",
                "peso": 0.75
            },
            {
                "id": 5,
                "texto": "¿Los servicios deben ser desplegados y actualizados de manera independiente?",
                "descripcion": "Determina si se necesitan ciclos de desarrollo y despliegue desacoplados.",
                "peso": 0.7
            }
        ]
    },
    {
        "categoria": "Disponibilidad, Integración y Escalabilidad Global",
        "descripcion": "Evalúa los aspectos globales del sistema en términos de disponibilidad y escalabilidad",
        "preguntas": [
            {
                "id": 6,
                "texto": "¿La aplicación requiere alta disponibilidad y resiliencia ante fallos?",
                "descripcion": "Se busca que el fallo de un módulo no provoque la caída del sistema completo.",
                "peso": 0.85
            },
            {
                "id": 7,
                "texto": "¿El sistema necesita integrarse con múltiples tecnologías o proveedores externos?",
                "descripcion": "Determina la flexibilidad e interoperabilidad requerida.",
                "peso": 0.75
            },
            {
                "id": 8,
                "texto": "¿El sistema debe permitir que múltiples equipos de desarrollo trabajen en paralelo?",
                "descripcion": "Facilita la división del trabajo sin generar cuellos de botella en el desarrollo.",
                "peso": 0.7
            },
            {
                "id": 9,
                "texto": "¿El sistema maneja una carga de trabajo variable y necesita optimización de recursos?",
                "descripcion": "Evalúa la capacidad de ajustar recursos según la demanda.",
                "peso": 0.8
            },
            {
                "id": 10,
                "texto": "¿La aplicación es lo suficientemente grande y compleja para justificar la separación en microservicios?",
                "descripcion": "Ayuda a determinar si la complejidad del dominio justifica la modularización.",
                "peso": 0.9
            },
            {
                "id": 11,
                "texto": "¿Existen múltiples reglas de negocio independientes que se puedan gestionar de forma separada?",
                "descripcion": "Identifica la necesidad de separar lógicas de negocio para facilitar el mantenimiento.",
                "peso": 0.75
            },
            {
                "id": 12,
                "texto": "¿El sistema maneja un alto volumen de transacciones y datos?",
                "descripcion": "Determina si es necesario distribuir la carga para mejorar el rendimiento.",
                "peso": 0.8
            },
            {
                "id": 13,
                "texto": "¿La aplicación requiere actualizaciones frecuentes en módulos específicos sin afectar al sistema completo?",
                "descripcion": "Permite valorar la independencia del ciclo de vida de cada componente.",
                "peso": 0.75
            }
        ]
    },
    {
        "categoria": "Arquitectura Orientada a Eventos",
        "descripcion": "Evalúa la necesidad de comunicación basada en eventos y procesamiento asíncrono",
        "preguntas": [
            {
                "id": 14,
                "texto": "¿El sistema se beneficiaría de la comunicación basada en eventos (procesamiento asíncrono, reintentos, tolerancia a fallos en la propagación de cambios)?",
                "descripcion": "Identifica si la comunicación asíncrona aporta ventajas en el flujo de procesos.",
                "peso": 0.85
            },
            {
                "id": 15,
                "texto": "¿El sistema necesita manejar eventos en tiempo real o casi en tiempo real?",
                "descripcion": "Evalúa la necesidad de procesamiento inmediato y respuesta ágil.",
                "peso": 0.8
            },
            {
                "id": 16,
                "texto": "¿El sistema debe permitir que múltiples consumidores reaccionen al mismo evento sin acoplar el origen al destino?",
                "descripcion": "Permite determinar si se requiere una comunicación desacoplada entre emisores y receptores.",
                "peso": 0.75
            },
            {
                "id": 17,
                "texto": "¿El sistema necesita manejar flujos de eventos complejos y orquestación de procesos mediante eventos?",
                "descripcion": "Identifica la necesidad de coordinar múltiples procesos o flujos de datos.",
                "peso": 0.7
            },
            {
                "id": 18,
                "texto": "¿Se requiere reducir la dependencia de bases de datos centralizadas y permitir la propagación de cambios en tiempo real?",
                "descripcion": "Evalúa si es ventajoso evitar bloqueos y centralización en la gestión de datos.",
                "peso": 0.65
            }
        ]
    }
]

# Mapeo de los resultados de lógica difusa
INTERPRETACION_DIFUSA = {
    "baja": (0, 0.33),
    "media": (0.34, 0.66),
    "alta": (0.67, 1.0)
}

# Reglas difusas para la recomendación de arquitecturas
REGLAS_DIFUSAS = [
    {
        "condicion": "Si la mayoría de preguntas de 'División y Autonomía de Servicios' tienen valor ALTO",
        "resultado": "Inclinación hacia microservicios"
    },
    {
        "condicion": "Si la mayoría de preguntas de 'Arquitectura Orientada a Eventos' tienen valor ALTO",
        "resultado": "Inclinación hacia arquitectura basada en eventos"
    },
    {
        "condicion": "Si la mayoría de preguntas de todas las categorías tienen valor BAJO",
        "resultado": "Inclinación hacia arquitectura monolítica"
    }
]
