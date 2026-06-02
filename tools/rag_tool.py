# ============================================================
# HERRAMIENTA 1: CONSULTA RAG - AGENTE RRHH FALABELLA
# Permite al agente buscar información en los documentos internos
# ============================================================

import os
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.tools import Tool

def consultar_documentos_rrhh(pregunta: str) -> str:
    """
    Busca información relevante en los documentos internos de RRHH
    usando búsqueda semántica en ChromaDB.
    """
    github_token = os.getenv("GITHUB_TOKEN")
    base_url = os.getenv("OPENAI_BASE_URL", "https://models.inference.ai.azure.com")

    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        openai_api_key=github_token,
        openai_api_base=base_url
    )

    vectorstore = Chroma(
        persist_directory="./chroma_db",
        embedding_function=embeddings
    )

    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4}
    )

    docs = retriever.invoke(pregunta)

    if not docs:
        return "No se encontró información relevante en los documentos de RRHH."

    contexto = "\n\n".join([doc.page_content for doc in docs])
    return f"Información encontrada en documentos RRHH:\n\n{contexto}"


rag_tool = Tool(
    name="consultar_documentos_rrhh",
    func=consultar_documentos_rrhh,
    description=(
        "Úsala cuando el empleado pregunta sobre políticas, beneficios, vacaciones, "
        "reglamento interno, permisos, accidentes laborales o cualquier tema de RRHH. "
        "Input: la pregunta del empleado en texto."
    )
)