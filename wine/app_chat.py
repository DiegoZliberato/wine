import streamlit as st
import google.generativeai as genai
import pdfplumber 
import time
API_KEY = ""
genai.configure(api_key=API_KEY)

st.markdown("<h1 style='text-align: center; color: white;'>ClarIA - MANAGER ASSISTANT</h1>", unsafe_allow_html=True)

# Función para leer PDF
def leer_pdf(file) -> str:
    texto = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            contenido = page.extract_text()
            if contenido:
                texto += contenido + "\n"
    return texto

# Inicializar modelo Gemini
if "model_chat" not in st.session_state:
    model = genai.GenerativeModel("gemini-2.0-flash", system_instruction="""
            Eres un agente llamado ClarIA especializado en traducir conceptos complejos de ciencia de datos, inteligencia artificial, programación y computación en la nube a un lenguaje claro, simple y enfocado al nivel gerencial.
            Tu función principal es ayudar a gerentes y tomadores de decisiones a comprender lo esencial de estos temas sin entrar en tecnicismos innecesarios, y enfocándote en impacto de negocio, beneficios, riesgos y toma de decisiones.
            Restricción: Solo puedes responder preguntas relacionadas con ciencia de datos, IA, programación y tecnologías en la nube. No debes responder preguntas fuera de estos ámbitos. (en caso tal pregunta de manera amigable si necesita ayuda sobre los temas anterior mente mesionados)
            Objetivo: Que un gerente no técnico pueda entender lo que su equipo técnico le está comunicando y tomar decisiones con confianza.
            Estilo de respuesta:
            •	Usa analogías del mundo empresarial si es útil.
            •	Evita jerga técnica o explíquela si es necesario de inmediato con un ejemplo sencillo.
            •	Si algo es complejo, divídelo en partes y usa ejemplos prácticos.
            •   Se formal y amigable a la hora de responder
            •	Enfócate en el “por qué importa” y “cómo impacta al negocio”.
            cada vez que termines una interaccion pregunta si la informacion fue clara y si necesita alguna otra pregunta
            optimiza el tiempo en respuesta
        """)
    st.session_state.model_chat = model.start_chat()


if "messages" not in st.session_state:
    st.session_state.messages = []

if "first_message" not in st.session_state:
    st.session_state.first_message = True


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if st.session_state.first_message:
    with st.chat_message("assistant"):
        st.markdown("Hola soy ClarIA, ¿en qué puedo ayudarte?")
    st.session_state.messages.append({"role":"assistant","content":"Hola soy ClarIA, ¿en qué puedo ayudarte?"})
    st.session_state.first_message = False




if pdf_file := st.file_uploader("Si quieres, puedes cargar un PDF para que lo resuma:", type=["pdf"]):
    
    texto_pdf = leer_pdf(pdf_file)

    if st.button("Resumir PDF"):
        prompt = (
            "Resume el siguiente documento en un lenguaje gerencial, "
            "en máximo de 45 lineas, resaltando solo lo más importante para la toma de decisiones:\n\n"
            + texto_pdf
        )
        respuesta = st.session_state.model_chat.send_message(prompt).text
        with st.chat_message("assistant"):
            st.markdown(respuesta)
            
        st.session_state.messages.append({"role":"assistant","content":respuesta})
        


# Chat tradicional

if question := st.chat_input("Escribe aquí tu consulta"):
    tiempo_inicio = time.time()
    with st.chat_message("user"):
        st.markdown(question)
    st.session_state.messages.append({"role":"user","content":question})

    result = st.session_state.model_chat.send_message(question).text
    with st.chat_message("assistant"):
        st.markdown(result)
        tiempo_final = time.time()
        tiempototal = tiempo_final - tiempo_inicio
        print (tiempototal)
    st.session_state.messages.append({"role":"assistant","content":result})