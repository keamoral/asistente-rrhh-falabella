# ============================================================
# HERRAMIENTA 4: ESCALACIÓN A RRHH - AGENTE RRHH FALABELLA
# Permite al agente derivar casos complejos al equipo humano
# ============================================================

from langchain_core.tools import Tool
from datetime import datetime


def escalar_a_rrhh(motivo: str) -> str:
    """
    Simula la derivación de un caso complejo al equipo de RRHH humano.
    Registra el motivo y entrega instrucciones al empleado.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    codigo_caso = f"CASO-{datetime.now().strftime('%Y%m%d%H%M%S')}"

    respuesta = (
        f"He registrado tu consulta para ser atendida por el equipo de RRHH.\n\n"
        f"Código de caso: {codigo_caso}\n"
        f"Fecha y hora: {timestamp}\n"
        f"Motivo: {motivo}\n\n"
        f"Canales de contacto disponibles:\n"
        f"  - Teléfono: 600 390 1111 (lunes a viernes, 9:00 a 18:00 hrs)\n"
        f"  - Correo: rrhh@falabella.cl\n"
        f"  - Portal interno: intranet.falabella.cl/rrhh\n\n"
        f"Un ejecutivo de RRHH se contactará contigo en un plazo máximo de 48 horas hábiles."
    )

    return respuesta


escalation_tool = Tool(
    name="escalar_a_rrhh",
    func=escalar_a_rrhh,
    description=(
        "Úsala cuando la consulta del empleado es demasiado compleja, sensible o específica "
        "como para responderla con los documentos disponibles. Por ejemplo: despidos, "
        "licencias médicas prolongadas, conflictos laborales, o situaciones legales. "
        "Input: descripción breve del motivo de escalación."
    )
)