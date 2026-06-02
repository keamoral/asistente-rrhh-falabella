# ============================================================
# HERRAMIENTA 3: REGISTRO DE CONSULTAS - AGENTE RRHH FALABELLA
# Permite al agente guardar y recuperar el historial persistente
# ============================================================

from langchain_core.tools import Tool
from memory.memory_config import guardar_en_largo_plazo, recuperar_historial_reciente


def registrar_consulta(entrada: str) -> str:
    """
    Guarda una consulta y su respuesta en el historial persistente.
    Formato esperado: "pregunta || respuesta"
    """
    if "||" not in entrada:
        return "Formato incorrecto. Usa: 'pregunta || respuesta'"

    partes = entrada.split("||", 1)
    pregunta = partes[0].strip()
    respuesta = partes[1].strip()

    resultado = guardar_en_largo_plazo(pregunta, respuesta)
    return resultado


def ver_historial(n: str = "5") -> str:
    """
    Recupera las últimas n consultas del historial persistente.
    """
    try:
        cantidad = int(n.strip())
    except ValueError:
        cantidad = 5

    return recuperar_historial_reciente(cantidad)


log_tool = Tool(
    name="registrar_consulta",
    func=registrar_consulta,
    description=(
        "Úsala para guardar en el historial persistente una consulta ya respondida. "
        "Input formato: 'pregunta del empleado || respuesta entregada'."
    )
)

historial_tool = Tool(
    name="ver_historial_consultas",
    func=ver_historial,
    description=(
        "Úsala cuando el empleado pregunta si ya consultó algo antes, o para revisar "
        "consultas previas registradas. Input: número de consultas a recuperar (ej: '5')."
    )
)