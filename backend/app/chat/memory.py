import json
from pathlib import Path

from langchain_core.messages import AIMessage, HumanMessage


CHAT_FILE = Path("backend/data/chat/current_session.json")


def load_history():
    if not CHAT_FILE.exists():
        return []

    with CHAT_FILE.open("r", encoding="utf-8") as file:
        messages = json.load(file)

    history = []

    for message in messages:
        if message["role"] == "user":
            history.append(
                HumanMessage(content=message["content"])
            )
        elif message["role"] == "assistant":
            history.append(
                AIMessage(content=message["content"])
            )

    return history


def save_message(role: str, content: str):
    CHAT_FILE.parent.mkdir(parents=True, exist_ok=True)

    messages = []

    if CHAT_FILE.exists():
        with CHAT_FILE.open("r", encoding="utf-8") as file:
            messages = json.load(file)

    messages.append(
        {
            "role": role,
            "content": content,
        }
    )

    with CHAT_FILE.open("w", encoding="utf-8") as file:
        json.dump(messages, file, indent=2)


def clear_history():
    CHAT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with CHAT_FILE.open("w", encoding="utf-8") as file:
        json.dump([], file, indent=2)