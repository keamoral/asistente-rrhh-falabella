# ============================================================
# CONFIGURACIÓN DE MEMORIA - AGENTE RRHH FALABELLA
# Memoria de corto plazo: historial de mensajes en sesión
# Memoria de largo plazo: JSON persistente
# ============================================================

import os
import json
from datetime import datetime

HISTORIAL_PATH = "./historial_consultas.json"

def guardar_en_largo_plazo(pregunta: str, respuesta: str):
    entrada = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "pregunta": pregunta,
        "respuesta": respuesta
    }

    historial = []
    if os.path.exists(HISTORIAL_PATH):
        with open(HISTORIAL_PATH, "r", encoding="utf-8") as f:
            historial = json.load(f)

    historial.append(entrada)

    with open(HISTORIAL_PATH, "w", encoding="utf-8") as f:
        json.dump(historial, f, ensure_ascii=False, indent=2)

    return f"Consulta registrada en historial ({len(historial)} total)"


def recuperar_historial_reciente(n: int = 5):
    if not os.path.exists(HISTORIAL_PATH):
        return "No hay historial previo registrado."

    with open(HISTORIAL_PATH, "r", encoding="utf-8") as f:
        historial = json.load(f)

    recientes = historial[-n:]
    if not recientes:
        return "No hay consultas registradas aún."

    resultado = "Últimas consultas registradas:\n"
    for entry in recientes:
        resultado += f"\n[{entry['timestamp']}]\n"
        resultado += f"  Pregunta: {entry['pregunta']}\n"
        resultado += f"  Respuesta: {entry['respuesta'][:100]}...\n"

    return resultado