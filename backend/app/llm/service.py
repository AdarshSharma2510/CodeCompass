from app.llm.model import llm
from app.llm.prompts import CODEBASE_PROMPT
from app.retrieval.retriever import retriever


def ask_codebase(question: str) -> str:
    documents = retriever.invoke(question)

    context = "\n\n".join(
        [
            (
                f"FILE: {document.metadata.get('file_path')}\n"
                f"{document.page_content}"
            )
            for document in documents
        ]
    )

    prompt = CODEBASE_PROMPT.invoke(
        {
            "context": context,
            "question": question,
        }
    )

    response = llm.invoke(prompt)

    return response.content