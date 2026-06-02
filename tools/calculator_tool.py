# ============================================================
# HERRAMIENTA 2: CALCULADORA DE BENEFICIOS - AGENTE RRHH FALABELLA
# Permite al agente realizar cálculos de vacaciones, sueldos, etc.
# ============================================================

from langchain_core.tools import Tool

def calcular_beneficios(consulta: str) -> str:
    """
    Realiza cálculos relacionados con beneficios laborales:
    - Días de vacaciones según años de servicio
    - Descuentos de empleado
    - Bonos y gratificaciones
    """
    consulta_lower = consulta.lower()

    # Cálculo de vacaciones según años de servicio
    if "vacacion" in consulta_lower or "días" in consulta_lower or "dias" in consulta_lower:
        for palabra in consulta_lower.split():
            if palabra.isdigit():
                años = int(palabra)
                if años < 1:
                    return "Con menos de 1 año de servicio no corresponden vacaciones legales."
                elif años < 3:
                    dias = 15
                elif años < 5:
                    dias = 17
                elif años < 10:
                    dias = 20
                else:
                    dias = 25
                return (
                    f"Con {años} año(s) de servicio en Falabella, "
                    f"corresponden {dias} días hábiles de vacaciones anuales."
                )
        return "Para calcular vacaciones, indica cuántos años llevas en la empresa. Ejemplo: 'calcular vacaciones 3 años'"

    # Cálculo de descuento de empleado
    if "descuento" in consulta_lower or "empleado" in consulta_lower:
        return (
            "Como empleado Falabella tienes:\n"
            "- 20% de descuento en tiendas Falabella\n"
            "- 15% de descuento en Sodimac\n"
            "- 10% de descuento en Tottus\n"
            "El descuento es acumulable con promociones salvo excepciones indicadas."
        )

    # Cálculo de gratificación
    if "gratificacion" in consulta_lower or "gratificación" in consulta_lower or "bono" in consulta_lower:
        return (
            "La gratificación legal en Chile corresponde al 25% de lo devengado "
            "en el año, con tope de 4.75 IMM anuales. Falabella la paga mensualmente "
            "de forma proporcional incluida en la liquidación."
        )

    return (
        "Puedo calcular: días de vacaciones por años de servicio, descuentos de empleado, "
        "o información sobre gratificaciones. ¿Qué necesitas calcular?"
    )


calculator_tool = Tool(
    name="calcular_beneficios",
    func=calcular_beneficios,
    description=(
        "Úsala cuando el empleado necesita calcular días de vacaciones según años de servicio, "
        "descuentos en tiendas, bonos o gratificaciones. "
        "Input: descripción del cálculo que se necesita, incluyendo números si aplica."
    )
)