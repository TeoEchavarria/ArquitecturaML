import streamlit as st
import json
import os
from utils.openai_helper import get_openai_response, cargar_contexto_arquitectura
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl

def app():
    st.title("Chat de Asesoría Arquitectónica")
    
    # Verificar si la encuesta fue completada
    if 'encuesta_completada' not in st.session_state or not st.session_state.encuesta_completada:
        st.warning("Por favor, completa la encuesta primero para recibir asesoría personalizada.")
        st.info("Ve a la página 'Encuesta' para comenzar la evaluación.")
        return
    
    # Mostrar resumen de resultados de la encuesta
    st.subheader("Resultados de tu Evaluación")
    
    resultados = st.session_state.resultados_encuesta
    
    # Crear un gráfico de resumen por categoría
    categorias = [cat for cat in resultados.keys() if cat not in ["puntuaciones_globales", "recomendacion"]]
    promedios = [resultados[cat]["promedio"] for cat in categorias]
    
    # Mostrar promedios por categoría
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label=categorias[0][:20] + "...", 
            value=f"{promedios[0]:.2f}", 
            delta=f"{'+' if promedios[0] > 0.5 else ''}{(promedios[0] - 0.5):.2f}"
        )
    
    with col2:
        st.metric(
            label=categorias[1][:20] + "...", 
            value=f"{promedios[1]:.2f}", 
            delta=f"{'+' if promedios[1] > 0.5 else ''}{(promedios[1] - 0.5):.2f}"
        )
    
    with col3:
        st.metric(
            label=categorias[2][:20] + "...", 
            value=f"{promedios[2]:.2f}", 
            delta=f"{'+' if promedios[2] > 0.5 else ''}{(promedios[2] - 0.5):.2f}"
        )
    
    # Mostrar puntuaciones globales en un gráfico de radar
    st.subheader("Valoración Estilo Arquitectónico")
    
    # Interpretación preliminar
    st.subheader("Recomendación de Arquitectura")
    
    # Mostrar la recomendación
    recomendacion = resultados["recomendacion"]
    st.markdown(f"### {recomendacion['descripcion']}")
    st.markdown(f"**Puntuación**: {recomendacion['puntuacion']:.2f}")
    st.markdown(f"_{recomendacion['mensaje']}_")
    
    # Si hay arquitecturas con puntuaciones cercanas, mencionarlas
    arquitecturas_cercanas_presentes = False
    if recomendacion['cercanas']:
        arquitecturas_cercanas_presentes = True
        st.info(f"También podrías considerar: {', '.join([arq.capitalize() for arq in recomendacion['cercanas']])}")
    
    # Interpretación textual (como estaba en el estado de sesión)
    st.write(st.session_state.interpretacion_preliminar)
    
    # Crear layout de dos columnas para el gráfico y el contexto
    col_grafico, col_contexto = st.columns([1, 1])
    
    with col_grafico:
        # Extraer puntuaciones para cada arquitectura
        puntuaciones = resultados["puntuaciones_globales"]
        
        # Crear nombres más claros para la visualización
        nombres_arquitecturas = {
            "microservicios": "Microservicios",
            "eventos": "Eventos",
            "monolitico": "Monolítica",
            "hibrido": "SOA"  # Cambiamos híbrido por SOA para adaptar a la imagen
        }
        
        # Preparar datos para el gráfico radar
        arquitecturas = [nombres_arquitecturas.get(arq, arq) for arq in puntuaciones.keys()]
        valores = [puntuaciones[arq] for arq in puntuaciones.keys()]
        
        # Crear valores ideales (1.0) para cada arquitectura
        valores_ideales = [1.0] * len(arquitecturas)
        
        # Crear valores mínimos (0.33) para cada arquitectura
        valores_minimos = [0.33] * len(arquitecturas)
        
        # Configurar el gráfico de radar
        fig = plt.figure(figsize=(6, 5))  # Tamaño reducido
        ax = fig.add_subplot(111, polar=True)
        
        # Configurar el estilo del gráfico
        plt.style.use('default')
        
        # Número de variables
        N = len(arquitecturas)
        
        # Calcular ángulos para cada eje (en radianes)
        angulos = [n / float(N) * 2 * np.pi for n in range(N)]
        
        # Cerrar el polígono repitiendo el primer ángulo
        angulos += angulos[:1]
        
        # Ajustar valores para cerrar el polígono
        valores += valores[:1]
        valores_ideales += valores_ideales[:1]
        valores_minimos += valores_minimos[:1]
        
        # Añadir los ejes
        plt.xticks(angulos[:-1], arquitecturas, size=10)  # Tamaño de texto reducido
        
        # Dibujar límites del gráfico
        ax.set_rlabel_position(0)
        plt.yticks([0.2, 0.4, 0.6, 0.8, 1.0], ["20%", "40%", "60%", "80%", "100%"], color="grey", size=8)  # Tamaño de texto reducido
        plt.ylim(0, 1)
        
        # Dibujar cada línea y rellenar área
        ax.plot(angulos, valores_ideales, linewidth=1, linestyle='dashed', color='blue', label='Ideal', alpha=0.9)
        ax.plot(angulos, valores, linewidth=2, linestyle='solid', color='green', label='Real', alpha=0.9)
        ax.plot(angulos, valores_minimos, linewidth=1, linestyle='dotted', color='red', label='Mínimo', alpha=0.9)
        
        # Rellenar áreas
        ax.fill(angulos, valores, color='green', alpha=0.2)
        
        # Añadir valores numéricos a los puntos del polígono real
        for i, valor in enumerate(valores[:-1]):  # Excluir el último que es repetido
            porcentaje = int(valor * 100)
            ax.annotate(f"{porcentaje}%", 
                       xy=(angulos[i], valor),
                       xytext=(angulos[i], valor + 0.05),
                       ha='center',
                       va='bottom',
                       bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.7),
                       fontsize=8)  # Tamaño de texto reducido
        
        # Añadir título y leyenda
        plt.title('VALORACIÓN ESTILO ARQUITECTÓNICO', size=12, y=1.1)  # Tamaño del título reducido
        plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1), fontsize=8)  # Tamaño de leyenda reducido
        
        # Mostrar gráfico en Streamlit
        st.pyplot(fig)

    with col_contexto:
        # Sección para mostrar el contexto de la arquitectura
        st.subheader("Información de referencia")
        
        # Obtener el contexto de la arquitectura recomendada
        arq_principal = recomendacion['tipo']
        contexto_principal = cargar_contexto_arquitectura(arq_principal)
        
        # Estilos CSS para el contenedor con altura limitada
        css_contenedor_limitado = """
        <style>
        .contenedor-limitado {
            height: 300px;
            overflow-y: hidden;
            position: relative;
            margin-bottom: 10px;
        }
        .contenedor-expandido {
            height: auto;
            overflow-y: visible;
        }
        .gradient-overlay {
            position: absolute;
            bottom: 0;
            left: 0;
            width: 100%;
            height: 50px;
            background: linear-gradient(to bottom, rgba(255,255,255,0), rgba(255,255,255,1));
            pointer-events: none;
        }
        .expand-button {
            margin-top: 10px;
            color: #4169E1;
            cursor: pointer;
            display: inline-block;
            font-weight: bold;
        }
        </style>
        """
        
        # Script JavaScript para expandir/contraer el contenido
        expand_script = """
        <script>
        function toggleExpand(containerId) {
            const container = document.getElementById(containerId);
            const overlay = document.getElementById(containerId + '-overlay');
            const button = document.getElementById(containerId + '-button');
            
            if (container.classList.contains('contenedor-expandido')) {
                container.classList.remove('contenedor-expandido');
                overlay.style.display = 'block';
                button.innerText = 'Ver más ↓';
            } else {
                container.classList.add('contenedor-expandido');
                overlay.style.display = 'none';
                button.innerText = 'Ver menos ↑';
            }
        }
        </script>
        """
        
        # ID único para cada contenedor
        container_id = f"contexto-{arq_principal}"
        
        # Crear pestañas para cada arquitectura relevante
        if arquitecturas_cercanas_presentes:
            # Si hay arquitecturas cercanas, crear pestañas para todas
            arq_cercanas = recomendacion['cercanas']
            
            # Crear nombre de pestañas
            nombres_arquitecturas = {
                "microservicios": "Microservicios",
                "eventos": "Arq. Eventos",
                "monolitico": "Monolítico",
                "hibrido": "Híbrido"
            }
            
            tabs = st.tabs([nombres_arquitecturas.get(arq_principal, "Principal")] + 
                        [nombres_arquitecturas.get(arq, arq.capitalize()) for arq in arq_cercanas])
            
            # Pestaña para arquitectura principal
            with tabs[0]:
                if contexto_principal:
                    st.markdown(css_contenedor_limitado, unsafe_allow_html=True)
                    st.markdown(expand_script, unsafe_allow_html=True)
                    
                    # Contenedor con altura limitada
                    st.markdown(f'<div id="{container_id}" class="contenedor-limitado">{contexto_principal}<div id="{container_id}-overlay" class="gradient-overlay"></div></div>', unsafe_allow_html=True)
                    
                    # Botón para expandir/contraer
                    st.markdown(f'<div class="expand-button" id="{container_id}-button" onclick="toggleExpand(\'{container_id}\')">Ver más ↓</div>', unsafe_allow_html=True)
                else:
                    st.warning(f"No se encontró información detallada para la arquitectura {arq_principal}.")
            
            # Pestañas para arquitecturas cercanas
            for i, arq in enumerate(arq_cercanas):
                with tabs[i+1]:
                    contexto = cargar_contexto_arquitectura(arq)
                    tab_container_id = f"contexto-{arq}"
                    
                    if contexto:
                        st.markdown(css_contenedor_limitado, unsafe_allow_html=True)
                        st.markdown(expand_script, unsafe_allow_html=True)
                        
                        # Contenedor con altura limitada
                        st.markdown(f'<div id="{tab_container_id}" class="contenedor-limitado">{contexto}<div id="{tab_container_id}-overlay" class="gradient-overlay"></div></div>', unsafe_allow_html=True)
                        
                        # Botón para expandir/contraer
                        st.markdown(f'<div class="expand-button" id="{tab_container_id}-button" onclick="toggleExpand(\'{tab_container_id}\')">Ver más ↓</div>', unsafe_allow_html=True)
                    else:
                        st.warning(f"No se encontró información detallada para la arquitectura {arq}.")
        else:
            # Si solo hay una arquitectura recomendada, mostrar su contexto directo con altura limitada
            if contexto_principal:
                st.markdown(css_contenedor_limitado, unsafe_allow_html=True)
                st.markdown(expand_script, unsafe_allow_html=True)
                
                # Contenedor con altura limitada
                st.markdown(f'<div id="{container_id}" class="contenedor-limitado">{contexto_principal}<div id="{container_id}-overlay" class="gradient-overlay"></div></div>', unsafe_allow_html=True)
                
                # Botón para expandir/contraer
                st.markdown(f'<div class="expand-button" id="{container_id}-button" onclick="toggleExpand(\'{container_id}\')">Ver más ↓</div>', unsafe_allow_html=True)
            else:
                st.warning(f"No se encontró información detallada para la arquitectura {arq_principal}.")
    
    # Sección de chat
    st.subheader("Consulta con nuestro Asesor de Arquitectura")
    
    # Inicializar historial de chat si no existe
    if 'messages' not in st.session_state:
        # Mensaje inicial basado en la interpretación
        mensaje_inicial = st.session_state.interpretacion_preliminar
        if arquitecturas_cercanas_presentes:
            mensaje_inicial += f"\n\nLas arquitecturas {recomendacion['tipo']} y {', '.join(recomendacion['cercanas'])} tienen puntuaciones muy cercanas, lo que indica que podrías beneficiarte de un enfoque híbrido que combine sus características."
        
        st.session_state.messages = [
            {"role": "assistant", "content": f"{mensaje_inicial} ¿Tienes alguna pregunta específica sobre esta recomendación o quieres más detalles sobre cómo implementar esta arquitectura?"}
        ]
    
    # Mostrar mensajes previos
    for message in st.session_state.messages:
        avatar = "🧑‍💻" if message["role"] == "user" else "🤖"
        with st.chat_message(message["role"], avatar=avatar):
            st.write(message["content"])
    
    # Entrada de nuevo mensaje
    if prompt := st.chat_input("Escribe tu pregunta sobre arquitectura..."):
        # Agregar mensaje del usuario al historial
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Mostrar mensaje del usuario
        with st.chat_message("user", avatar="🧑‍💻"):
            st.write(prompt)
        
        # Preparar contexto básico para la API de OpenAI
        context = {
            "resultados_encuesta": resultados,
            "interpretacion_preliminar": st.session_state.interpretacion_preliminar,
            "historial_chat": st.session_state.messages[:-1]  # Todo el historial excepto el último mensaje
        }
        
        # Si hay arquitecturas con puntuaciones cercanas, agregar contexto adicional
        if arquitecturas_cercanas_presentes:
            # Determinar qué arquitecturas tienen puntuaciones cercanas
            arq_principal = recomendacion['tipo']
            arq_cercanas = recomendacion['cercanas']
            
            # Preparar contexto expandido con información sobre las arquitecturas cercanas
            context["tiene_arquitecturas_cercanas"] = True
            context["arquitectura_principal"] = arq_principal
            context["arquitecturas_cercanas"] = arq_cercanas
            
            # Añadir guía específica para el chatbot sobre cómo abordar un escenario híbrido
            context["guia_hibrida"] = """
            Este caso presenta varias arquitecturas con puntuaciones muy cercanas. 
            Al responder, considera las ventajas de cada enfoque y cómo podrían combinarse.
            Explora patrones de integración específicos que permitan aprovechar lo mejor de cada arquitectura.
            Sugiere estrategias para una implementación incremental que permita evolucionar desde una arquitectura a otra.
            Explica los compromisos y desafíos al combinar diferentes enfoques arquitectónicos.
            """
        else:
            context["tiene_arquitecturas_cercanas"] = False
        
        # Obtener respuesta del modelo
        response = get_openai_response(prompt, context)
        
        # Agregar respuesta del asistente al historial
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Mostrar respuesta del asistente
        with st.chat_message("assistant", avatar="🤖"):
            st.write(response)

if __name__ == "__main__":
    app()
