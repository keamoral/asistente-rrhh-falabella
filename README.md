# Asistente Virtual RRHH Falabella 🤖
**Proyecto ISY0101 - Ingeniería de Soluciones con IA**  
**DuocUC - 2025**  
**Integrantes:** Kevin Morales | Matías Damico

---

## Descripción

Agente conversacional de Recursos Humanos desarrollado para Falabella Retail S.A., capaz de responder consultas laborales de empleados mediante un pipeline RAG (Retrieval-Augmented Generation) potenciado con un agente ReAct que integra herramientas de consulta, cálculo, registro y escalación.

---

## Arquitectura del Sistema

```
[Empleado]
    ↓
[Agente ReAct - LangGraph]
    ├── 🔍 RAG Tool         → Consulta documentos internos (ChromaDB)
    ├── 🧮 Calculator Tool  → Calcula vacaciones, descuentos, bonos
    ├── 📝 Log Tool         → Registra consultas (memoria largo plazo)
    ├── 📋 Historial Tool   → Recupera consultas anteriores
    └── 🚨 Escalation Tool  → Deriva casos complejos a RRHH humano
         ↓
[Memoria Corto Plazo]     [Memoria Largo Plazo]
(historial_sesion[])      (historial_consultas.json)
```

---

## Tecnologías utilizadas

| Componente | Tecnología |
|---|---|
| Lenguaje | Python 3.x |
| Framework Agente | LangGraph + LangChain |
| Modelo LLM | GPT-4o-mini (GitHub Models) |
| Base de datos vectorial | ChromaDB |
| Embeddings | text-embedding-3-small (OpenAI) |
| Memoria largo plazo | JSON persistente |

---

## Estructura del proyecto

```
asistente-rrhh-falabella/
├── agent_rrhh.py                  ← Agente principal (EP2)
├── rag_pipeline.py                ← Pipeline RAG base (EP1)
├── tools/
│   ├── rag_tool.py                ← Herramienta de consulta RAG
│   ├── calculator_tool.py         ← Herramienta de cálculo de beneficios
│   ├── log_tool.py                ← Herramienta de registro persistente
│   └── escalation_tool.py         ← Herramienta de escalación a RRHH
├── memory/
│   └── memory_config.py           ← Configuración de memoria
├── chroma_db/                     ← Base de datos vectorial (generada)
├── historial_consultas.json       ← Historial persistente (generado)
├── reglamento_interno.txt
├── manual_beneficios.txt
├── politica_vacaciones_permisos.txt
├── faq_rrhh.txt
├── .env                           ← Variables de entorno (no subir a Git)
└── requirements.txt
```

---

## Instalación y ejecución

### 1. Clonar el repositorio
```bash
git clone https://github.com/keamoral/asistente-rrhh-falabella.git
cd asistente-rrhh-falabella
```

### 2. Crear entorno virtual
```bash
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Linux/Mac
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno
Crear archivo `.env` en la raíz del proyecto:
```
GITHUB_TOKEN=tu_github_token_aqui
OPENAI_BASE_URL=https://models.inference.ai.azure.com
```

> El token de GitHub debe tener acceso a GitHub Models (scope `repo`).

### 5. Ejecutar el agente
```bash
python agent_rrhh.py
```

---

## Herramientas del agente

| Herramienta | Cuándo se activa |
|---|---|
| `consultar_documentos_rrhh` | Preguntas sobre políticas, beneficios, reglamento |
| `calcular_beneficios` | Cálculos de vacaciones, descuentos, bonos |
| `registrar_consulta` | Al finalizar cada respuesta exitosa |
| `ver_historial_consultas` | Cuando el empleado pregunta por consultas previas |
| `escalar_a_rrhh` | Casos complejos, legales o sensibles |

---

## Memoria del agente

- **Corto plazo:** historial de mensajes de la sesión actual (ventana de 10 mensajes)
- **Largo plazo:** archivo `historial_consultas.json` con timestamp, pregunta y respuesta de cada interacción

---

## Referencias

- LangChain Docs. (2024). *LangChain Documentation*. https://python.langchain.com
- LangGraph Docs. (2024). *LangGraph Documentation*. https://langchain-ai.github.io/langgraph
- OpenAI. (2024). *GitHub Models - GPT-4o-mini*. https://github.com/marketplace/models
- Chroma. (2024). *ChromaDB Documentation*. https://docs.trychroma.com
