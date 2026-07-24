from app.chat.memory import load_history, save_message
from app.llm.model import llm
from app.llm.prompts import CODEBASE_QA_PROMPT
from app.retrieval.retriever import retriever


def ask_codebase(question: str) -> str:
    history = load_history()

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

    history_text = "\n\n".join(
        [
            f"{message.type.upper()}: {message.content}"
            for message in history
        ]
    )

    prompt = CODEBASE_QA_PROMPT.invoke(
        {
            "history": history_text,
            "context": context,
            "question": question,
        }
    )

    response = llm.invoke(prompt)

    answer = response.content

    save_message("user", question)
    save_message("assistant", answer)

    return answer