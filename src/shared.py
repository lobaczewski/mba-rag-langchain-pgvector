import os
import psycopg
from dotenv import load_dotenv

from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI

PROMPT_TEMPLATE = """CONTEXTO:
{context}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{question}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""


def build_prompt(context: str, question: str) -> str:
    return PROMPT_TEMPLATE.format(context=context, question=question)


def get_connection_string() -> str:
    # garante que .env foi carregado (ingest/chat chamam isso também)
    load_dotenv()

    host = os.getenv("PG_HOST", "localhost")
    port = os.getenv("PG_PORT", "5432")
    db = os.getenv("PG_DATABASE", "ragdb")
    user = os.getenv("PG_USER", "postgres")
    pwd = os.getenv("PG_PASSWORD", "postgres")

    # usado pelo langchain_postgres (SQLAlchemy+psycopg)
    return f"postgresql+psycopg://{user}:{pwd}@{host}:{port}/{db}"


def ensure_pgvector_extension(conn_str: str) -> None:
    # psycopg conecta melhor com postgresql:// (sem +psycopg)
    psycopg_conn = conn_str.replace("postgresql+psycopg://", "postgresql://")

    with psycopg.connect(psycopg_conn) as conn:
        with conn.cursor() as cur:
            cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
        conn.commit()


def _get_provider() -> str:
    provider = (os.getenv("PROVIDER", "openai") or "openai").strip().lower()
    if provider not in ("openai", "gemini"):
        raise ValueError("PROVIDER deve ser 'openai' ou 'gemini'.")
    return provider


def get_embeddings():
    load_dotenv()
    provider = _get_provider()

    if provider == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        model = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
        if not api_key:
            raise ValueError("OPENAI_API_KEY não configurada no .env")
        return OpenAIEmbeddings(model=model, api_key=api_key)

    api_key = os.getenv("GOOGLE_API_KEY")
    model = os.getenv("GEMINI_EMBEDDING_MODEL", "models/embedding-001")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY não configurada no .env")
    return GoogleGenerativeAIEmbeddings(model=model, google_api_key=api_key)


def get_llm():
    load_dotenv()
    provider = _get_provider()

    if provider == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        model = os.getenv("OPENAI_CHAT_MODEL", "gpt-5-nano")
        if not api_key:
            raise ValueError("OPENAI_API_KEY não configurada no .env")
        return ChatOpenAI(model=model, api_key=api_key, temperature=0)

    api_key = os.getenv("GOOGLE_API_KEY")
    model = os.getenv("GEMINI_CHAT_MODEL", "gemini-2.5-flash-lite")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY não configurada no .env")
    return ChatGoogleGenerativeAI(model=model, google_api_key=api_key, temperature=0)