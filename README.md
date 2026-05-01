# 🤖 Asistente RRHH Falabella - Pipeline RAG

**ISY0101 - Ingeniería de Soluciones con IA**  
**Duoc UC - 2025**

## 📋 Descripción

Sistema de agente inteligente basado en **RAG (Retrieval-Augmented Generation)** que responde preguntas de empleados de Falabella Retail S.A. sobre temas de Recursos Humanos, basándose exclusivamente en documentos internos oficiales de la empresa.

## 🏢 Caso Organizacional

**Empresa:** Falabella Retail S.A.  
**Problema:** El área de RRHH recibe diariamente cientos de consultas repetitivas sobre vacaciones, beneficios, licencias y reglamento interno, saturando al equipo de Personas.  
**Solución:** Agente con LLM y RAG que responde estas consultas de forma inmediata, precisa y disponible las 24 horas.

## 🗂️ Estructura del Proyecto

```
asistente-rrhh-falabella/
├── rag_pipeline.py                  # Pipeline RAG principal (ejecución local)
├── asistente_rrhh_falabella.ipynb   # Notebook para Google Colab
├── prompts_optimizados.txt          # Prompts diseñados con técnicas de Prompt Engineering
├── reglamento_interno.txt           # Documento interno simulado - Reglamento
├── manual_beneficios.txt            # Documento interno simulado - Beneficios
├── politica_vacaciones_permisos.txt # Documento interno simulado - Vacaciones
├── faq_rrhh.txt                     # Preguntas frecuentes de RRHH
└── README.md                        # Este archivo
```

## ⚙️ Tecnologías utilizadas

- **LangChain** — Framework principal para construir el pipeline RAG
- **ChromaDB** — Base de datos vectorial para almacenar embeddings
- **GitHub Models (GPT-4o-mini)** — Modelo de lenguaje para generación de respuestas
- **OpenAI Embeddings (text-embedding-3-small)** — Modelo para crear embeddings
- **Python 3.14** — Lenguaje de programación

## 🚀 Instrucciones de ejecución

### Opción 1 — Ejecución local (archivo .py)

**1. Clonar el repositorio**
```bash
git clone https://github.com/keamoral/asistente-rrhh-falabella.git
cd asistente-rrhh-falabella
```

**2. Crear y activar entorno virtual**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

**3. Instalar dependencias**
```bash
pip install langchain langchain-openai langchain-community chromadb openai python-dotenv langchain-text-splitters
```

**4. Configurar credenciales**

Crear un archivo `.env` en la carpeta del proyecto con el siguiente contenido:
```
GITHUB_TOKEN=tu_github_token_aqui
OPENAI_API_KEY=tu_github_token_aqui
OPENAI_BASE_URL=https://models.inference.ai.azure.com
```

> Para obtener un GitHub Token gratuito: github.com → Settings → Developer settings → Personal access tokens → Generate new token (classic)

**5. Ejecutar el pipeline**
```bash
python rag_pipeline.py
```

---

### Opción 2 — Google Colab (archivo .ipynb)

1. Abrir [Google Colab](https://colab.research.google.com)
2. Ir a **Archivo → Subir notebook**
3. Subir el archivo `asistente_rrhh_falabella.ipynb`
4. En la **Celda 2**, reemplazar `TU_GITHUB_TOKEN_AQUI` con tu token real
5. Hacer clic en **Ejecutar todo** ▶️

## 💬 Prompts implementados

El sistema utiliza 3 prompts diseñados con técnicas de Prompt Engineering:

| Prompt | Técnica | Uso |
|--------|---------|-----|
| System Prompt | Zero-shot con rol | Comportamiento general del asistente |
| Consulta de Beneficios | Few-shot | Preguntas sobre beneficios corporativos |
| Vacaciones y Permisos | Chain-of-Thought | Consultas con razonamiento condicional |

Ver detalle completo en `prompts_optimizados.txt`

## 🧪 Ejemplos de uso

```
👤 Empleado: ¿Cuántos días de vacaciones me corresponden si llevo 5 años?
🤖 Asistente: Si llevas 5 años en la empresa, te corresponden 15 días hábiles de vacaciones.

👤 Empleado: ¿Tengo descuento en tiendas Falabella?
🤖 Asistente: Sí, tienes un descuento del 15% en Falabella, Sodimac y Tottus con tu credencial de empleado.

👤 Empleado: ¿Qué hago si tuve un accidente en el trabajo?
🤖 Asistente: Debes informar de inmediato a tu supervisor. Serás derivado a la ACHS. No abandones el lugar sin reportarlo.
```

## 📚 Referencias

- LangChain Documentation: https://python.langchain.com/docs/
- GitHub Models Documentation: https://docs.github.com/en/github-models
- ChromaDB Documentation: https://docs.trychroma.com/
- RAG Architecture: https://www.pinecone.io/learn/retrieval-augmented-generation/
