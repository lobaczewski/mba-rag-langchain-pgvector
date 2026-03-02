# Desafio MBA — Ingestão e Busca Semântica com LangChain + Postgres (pgVector)

Este projeto implementa um pipeline RAG (Retrieval Augmented Generation) para:
1) **Ingerir** um PDF (`document.pdf`) em chunks e armazenar embeddings em **PostgreSQL + pgVector**
2) **Buscar** por similaridade (k=10) e responder via **CLI**, seguindo regras para **não inventar** respostas

---

## ✅ Requisitos

- Linux (ou WSL2)
- Docker + Docker Compose
- Python 3.10+ (recomendado 3.11+)

---

## 📁 Estrutura do projeto
