
# 📘 Desafio MBA — Ingestão e Busca Semântica com LangChain + Postgres (pgVector)

🎯 Objetivo

Este projeto implementa um pipeline RAG (Retrieval-Augmented Generation) capaz de:

Ingerir um PDF (document.pdf)

Dividir em chunks de 1000 caracteres

Utilizar overlap de 150

Gerar embeddings

Armazenar vetores no PostgreSQL + pgVector

Realizar busca semântica via CLI

Vetorizar a pergunta do usuário

Buscar os 10 resultados mais relevantes (k=10)

Construir o contexto a partir do banco vetorial

Responder somente com base no conteúdo do PDF

Nunca inventar respostas





🧠 Arquitetura

Fluxo do sistema:

PDF → Chunking → Embeddings → PostgreSQL + pgVector
                              ↓
Pergunta → Embedding → Similarity Search (k=10) → Prompt → LLM → Resposta
✅ Requisitos

Linux ou WSL2

Docker + Docker Compose

Python 3.10+ (recomendado 3.11+)

## 📁 Estrutura do Projeto
```
.
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── document.pdf
└── src/
    ├── __init__.py
    ├── ingest.py
    ├── search.py
    ├── chat.py
    └── shared.py
```

⚙️ Configuração do Ambiente
1️⃣ Subir o Banco de Dados (Postgres + pgVector)
docker compose up -d

Verificar se está rodando:

docker ps
2️⃣ Criar ambiente virtual Python
python3 -m venv venv
source venv/bin/activate

Instalar dependências:

pip install -r requirements.txt
3️⃣ Configurar variáveis de ambiente

Criar o arquivo .env:

cp .env.example .env

Editar .env e inserir sua chave de API.

Exemplo (OpenAI):

PROVIDER=openai
OPENAI_API_KEY=SUA_CHAVE_AQUI
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
OPENAI_CHAT_MODEL=gpt-5-nano

PG_HOST=localhost
PG_PORT=5432
PG_DATABASE=ragdb
PG_USER=postgres
PG_PASSWORD=postgres
PG_COLLECTION=pdf_chunks
🚀 Execução do Projeto
1️⃣ Ingestão do PDF

Certifique-se de que o arquivo document.pdf está na raiz do projeto.

Execute:

python -m src.ingest

Saída esperada:

Ingestão concluída!
PDF: document.pdf
Páginas carregadas: X
Chunks gerados: Y
Coleção: pdf_chunks
2️⃣ Executar o Chat (CLI)
python -m src.chat

Exemplo de uso:

PERGUNTA: Qual o faturamento da empresa?
RESPOSTA: ...
🔒 Regras de Resposta

O sistema segue as seguintes regras:

Utiliza similarity_search_with_score(query, k=10)

Responde apenas com base no CONTEXTO recuperado do banco vetorial

Se a informação não estiver explicitamente no contexto, retorna:

Não tenho informações necessárias para responder sua pergunta.

Nunca utiliza conhecimento externo

Nunca produz opiniões

🧪 Testes de Validação
Pergunta dentro do contexto:

Deve responder corretamente com base no PDF.

Pergunta fora do contexto:
Qual é a capital da França?

Resposta esperada:

Não tenho informações necessárias para responder sua pergunta.
🧰 Tecnologias Utilizadas

Python

LangChain

PostgreSQL

pgVector

Docker

OpenAI ou Gemini API

📌 Observações

O arquivo .env não é versionado.

O projeto pode ser executado do zero com:

docker compose down -v
docker compose up -d
python -m src.ingest
python -m src.chat
🎓 Conclusão

O projeto implementa corretamente um sistema de busca semântica baseado em RAG, garantindo:

Separação clara entre ingestão e busca

Armazenamento vetorial com pgVector

Recuperação por similaridade (k=10)

Controle de alucinação via prompt estruturado