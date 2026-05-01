# ============================================================
# PIPELINE RAG - ASISTENTE RRHH FALABELLA
# Proyecto: ISY0101 - Ingeniería de Soluciones con IA
# ============================================================

import os
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# ============================================================
# 1. CARGAR VARIABLES DE ENTORNO
# ============================================================
load_dotenv()
github_token = os.getenv("GITHUB_TOKEN")
base_url = os.getenv("OPENAI_BASE_URL", "https://models.inference.ai.azure.com")

if not github_token:
    raise ValueError("No se encontró el GITHUB_TOKEN. Verifica tu archivo .env")

print("✅ GitHub Token cargado correctamente")

# ============================================================
# 2. CARGAR DOCUMENTOS DE RRHH (FUENTES INTERNAS)
# ============================================================
print("\n📂 Cargando documentos de RRHH...")

documentos_rrhh = [
    "reglamento_interno.txt",
    "manual_beneficios.txt",
    "politica_vacaciones_permisos.txt",
    "faq_rrhh.txt"
]

documentos = []
for archivo in documentos_rrhh:
    loader = TextLoader(archivo, encoding="utf-8")
    docs = loader.load()
    documentos.extend(docs)
    print(f"  ✅ {archivo} cargado ({len(docs)} documento/s)")

print(f"\n📄 Total documentos cargados: {len(documentos)}")

# ============================================================
# 3. DIVIDIR DOCUMENTOS EN CHUNKS (FRAGMENTOS)
# ============================================================
print("\n✂️  Dividiendo documentos en fragmentos...")

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    separators=["\n\n", "\n", ".", " "]
)

chunks = text_splitter.split_documents(documentos)
print(f"✅ Total fragmentos creados: {len(chunks)}")

# ============================================================
# 4. CREAR EMBEDDINGS Y BASE DE DATOS VECTORIAL (ChromaDB)
# ============================================================
print("\n🔢 Creando embeddings y base de datos vectorial...")

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small",
    openai_api_key=github_token,
    openai_api_base=base_url
)

vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="./chroma_db"
)

print("✅ Base de datos vectorial creada en ./chroma_db")

# ============================================================
# 5. CONFIGURAR EL RETRIEVER
# ============================================================
retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 4}
)

# ============================================================
# 6. DEFINIR EL PROMPT OPTIMIZADO PARA RRHH
# ============================================================
prompt_template = """
Eres un asistente virtual de Recursos Humanos de Falabella Retail S.A.
Tu rol es responder preguntas de los empleados de manera clara, precisa y amable.

Reglas importantes:
- Responde ÚNICAMENTE basándote en la información de los documentos proporcionados.
- Si la información no está en los documentos, responde: "Lo siento, no tengo información sobre ese tema. Te recomiendo contactar directamente al equipo de RRHH al 600 390 1111."
- Usa un tono profesional pero cercano.
- Si la respuesta incluye números, fechas o montos, asegúrate de citarlos exactamente como aparecen en los documentos.
- No inventes información que no esté en los documentos.

Contexto de los documentos:
{context}

Pregunta del empleado: {question}

Respuesta:
"""

PROMPT = PromptTemplate(
    template=prompt_template,
    input_variables=["context", "question"]
)

# ============================================================
# 7. CONFIGURAR EL MODELO LLM (GitHub Models - Gratuito)
# ============================================================
print("\n🤖 Configurando el modelo LLM...")

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    openai_api_key=github_token,
    openai_api_base=base_url
)

# ============================================================
# 8. CREAR LA CADENA RAG
# ============================================================
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | PROMPT
    | llm
    | StrOutputParser()
)

print("✅ Pipeline RAG configurado correctamente")

# ============================================================
# 9. FUNCIÓN PARA HACER CONSULTAS
# ============================================================
def consultar_rrhh(pregunta):
    print(f"\n{'='*60}")
    print(f"👤 Empleado pregunta: {pregunta}")
    print(f"{'='*60}")
    respuesta = rag_chain.invoke(pregunta)
    print(f"🤖 Asistente RRHH responde:\n{respuesta}")
    return respuesta

# ============================================================
# 10. PRUEBAS DEL SISTEMA (5 PREGUNTAS DE EJEMPLO)
# ============================================================
print("\n" + "="*60)
print("🚀 INICIANDO PRUEBAS DEL ASISTENTE RRHH FALABELLA")
print("="*60)

preguntas_prueba = [
    "¿Cuántos días de vacaciones me corresponden si llevo 5 años en la empresa?",
    "¿Cuándo se paga el sueldo cada mes?",
    "¿Tengo descuento en tiendas Falabella como empleado?",
    "¿Qué hago si tuve un accidente en el trabajo?",
    "¿Puedo tomar vacaciones en diciembre?"
]

for pregunta in preguntas_prueba:
    consultar_rrhh(pregunta)

# ============================================================
# 11. MODO INTERACTIVO
# ============================================================
print("\n" + "="*60)
print("💬 MODO INTERACTIVO - Escribe 'salir' para terminar")
print("="*60)

while True:
    pregunta = input("\n👤 Tu pregunta: ").strip()
    if pregunta.lower() in ["salir", "exit", "quit"]:
        print("👋 ¡Hasta luego!")
        break
    if pregunta:
        consultar_rrhh(pregunta)
