import os
from dotenv import load_dotenv
from langchain_postgres import PGVector

from src.shared import get_connection_string, get_embeddings


def get_vectorstore() -> PGVector:
    load_dotenv()
    conn_str = get_connection_string()
    collection = os.getenv("PG_COLLECTION", "pdf_chunks")
    embeddings = get_embeddings()

    return PGVector(
        embeddings=embeddings,
        collection_name=collection,
        connection=conn_str,
        use_jsonb=True,
    )


def search_with_scores(query: str, k: int = 10):
    """Retorna lista de (Document, score) usando similarity_search_with_score."""
    vs = get_vectorstore()
    return vs.similarity_search_with_score(query, k=k)