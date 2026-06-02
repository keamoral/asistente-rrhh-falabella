# ============================================================
# AGENTE RRHH FALABELLA - EP2
# Proyecto: ISY0101 - Ingeniería de Soluciones con IA
# Agente ReAct con memoria de corto y largo plazo
# ============================================================

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage, SystemMessage

from tools.rag_tool import rag_tool
from tools.calculator_tool import calculator_tool
from tools.log_tool import log_tool, historial_tool
from tools.escalation_tool import escalation_tool
from memory.memory_config import guardar_en_largo_plazo, recuperar_historial_reciente

# Suprimir warnings de deprecación
import warnings
warnings.filterwarnings("ignore")

# ============================================================
# 1. CARGAR VARIABLES DE ENTORNO
# ============================================================
load_dotenv()
github_token = os.getenv("GITHUB_TOKEN")
base_url = os.getenv("OPENAI_BASE_URL", "https://models.inference.ai.azure.com")

if not github_token:
    raise ValueError("No se encontró el GITHUB_TOKEN. Verifica tu archivo .env")

print("✅ Variables de entorno cargadas")

# ============================================================
# 2. CONFIGURAR EL MODELO LLM
# ============================================================
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    openai_api_key=github_token,
    openai_api_base=base_url
)

print("✅ Modelo LLM configurado")

# ============================================================
# 3. DEFINIR HERRAMIENTAS DEL AGENTE
# ============================================================
tools = [
    rag_tool,
    calculator_tool,
    log_tool,
    historial_tool,
    escalation_tool
]

print(f"✅ {len(tools)} herramientas registradas")

# ============================================================
# 4. PROMPT DEL SISTEMA
# ============================================================
system_prompt = """Eres un asistente virtual de Recursos Humanos de Falabella Retail S.A.
Tu rol es responder preguntas de los empleados de manera clara, precisa y amable.

Reglas importantes:
- Usa SIEMPRE la herramienta consultar_documentos_rrhh como primera opción para preguntas de RRHH.
- Usa calcular_beneficios cuando el empleado necesite un cálculo específico con números.
- Usa escalar_a_rrhh cuando la consulta sea compleja, legal o sensible.
- Usa registrar_consulta al finalizar CADA respuesta exitosa para guardar el historial.
- Usa ver_historial_consultas si el empleado pregunta por consultas anteriores.
- Responde siempre en español con tono profesional y cercano.
- Si no encuentras información en los documentos, escala a RRHH en lugar de inventar.
"""

# ============================================================
# 5. CREAR EL AGENTE ReAct (LangGraph)
# ============================================================
agent_executor = create_react_agent(
    model=llm,
    tools=tools,
    prompt=system_prompt
)

print("✅ Agente ReAct creado y listo")

# ============================================================
# 6. MEMORIA DE CORTO PLAZO (historial de mensajes en sesión)
# ============================================================
historial_sesion = []

# ============================================================
# 7. FUNCIÓN PRINCIPAL DE CONSULTA
# ============================================================
def consultar_agente(pregunta: str) -> str:
    global historial_sesion

    print(f"\n{'='*60}")
    print(f"👤 Empleado: {pregunta}")
    print(f"{'='*60}")

    # Agrega la pregunta al historial de sesión (memoria corto plazo)
    historial_sesion.append(HumanMessage(content=pregunta))

    # Limita a las últimas 5 interacciones (ventana de memoria)
    mensajes_ventana = historial_sesion[-10:]

    resultado = agent_executor.invoke({"messages": mensajes_ventana})
    mensajes_respuesta = resultado.get("messages", [])

    # Extrae la última respuesta del agente
    respuesta = ""
    for msg in reversed(mensajes_respuesta):
        if hasattr(msg, "content") and msg.content and not hasattr(msg, "tool_calls"):
            respuesta = msg.content
            break

    if not respuesta:
        respuesta = "No se pudo obtener una respuesta."

    # Guarda la respuesta en el historial de sesión
    from langchain_core.messages import AIMessage
    historial_sesion.append(AIMessage(content=respuesta))

    # Guarda en memoria de largo plazo
    guardar_en_largo_plazo(pregunta, respuesta)

    print(f"\n🤖 Agente RRHH: {respuesta}")
    return respuesta

# ============================================================
# 8. PRUEBAS DEL AGENTE
# ============================================================
if __name__ == "__main__":
    print("\n" + "="*60)
    print("🚀 INICIANDO AGENTE RRHH FALABELLA - EP2")
    print("="*60)

    preguntas_prueba = [
        "¿Cuántos días de vacaciones me corresponden si llevo 5 años en la empresa?",
        "¿Cuándo se paga el sueldo cada mes?",
        "Tengo un conflicto grave con mi jefatura, ¿qué puedo hacer?",
        "¿Cuántas vacaciones me corresponden si llevo 3 años?",
        "¿Me puedes mostrar mis consultas anteriores?"
    ]

    for pregunta in preguntas_prueba:
        consultar_agente(pregunta)

    print("\n" + "="*60)
    print("💬 MODO INTERACTIVO - Escribe 'salir' para terminar")
    print("="*60)

    while True:
        pregunta = input("\n👤 Tu pregunta: ").strip()
        if pregunta.lower() in ["salir", "exit", "quit"]:
            print("👋 ¡Hasta luego!")
            break
        if pregunta:
            consultar_agente(pregunta)