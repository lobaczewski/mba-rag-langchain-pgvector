import os
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_postgres import PGVector

from src.shared import get_connection_string, get_embeddings, ensure_pgvector_extension

PDF_PATH = os.getenv("PDF_PATH", "document.pdf")


def main() -> None:
    load_dotenv()

    conn_str = get_connection_string()
    collection = os.getenv("PG_COLLECTION", "pdf_chunks")

    ensure_pgvector_extension(conn_str)

    if not os.path.exists(PDF_PATH):
        raise FileNotFoundError(f"PDF não encontrado em: {PDF_PATH}")

    loader = PyPDFLoader(PDF_PATH)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
        separators=["\n\n", "\n", " ", ""],
    )
    chunks = splitter.split_documents(docs)

    embeddings = get_embeddings()

    vectorstore = PGVector(
        embeddings=embeddings,
        collection_name=collection,
        connection=conn_str,
        use_jsonb=True,
    )

    vectorstore.add_documents(chunks)

    print("✅ Ingestão concluída!")
    print(f"- PDF: {PDF_PATH}")
    print(f"- Páginas carregadas: {len(docs)}")
    print(f"- Chunks gerados: {len(chunks)}")
    print(f"- Coleção: {collection}")


if __name__ == "__main__":
    main()