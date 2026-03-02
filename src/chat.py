import os
from dotenv import load_dotenv

from src.search import search_with_scores
from src.shared import build_prompt, get_llm


def main() -> None:
    load_dotenv()
    llm = get_llm()

    print("=== Chat RAG (PDF) ===")
    print("Digite sua pergunta. Para sair, digite: exit\n")

    while True:
        user_q = input("PERGUNTA: ").strip()

        if not user_q:
            continue

        if user_q.lower() in ("exit", "quit", "sair"):
            print("Bye!")
            break

        results = search_with_scores(user_q, k=10)

        context_parts = []
        for doc, _score in results:
            context_parts.append(doc.page_content)

        context = "\n\n---\n\n".join(context_parts)
        prompt = build_prompt(context=context, question=user_q)

        answer = llm.invoke(prompt)
        text = answer if isinstance(answer, str) else getattr(answer, "content", str(answer))

        print(f"RESPOSTA: {text.strip()}\n")


if __name__ == "__main__":
    main()