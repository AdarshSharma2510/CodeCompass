from fastapi import APIRouter
from pydantic import BaseModel

from app.llm.service import ask_codebase
from app.chat.memory import clear_history

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


class ChatRequest(BaseModel):
    question: str


class ChatResponse(BaseModel):
    answer: str


@router.post("", response_model=ChatResponse)
def chat(request: ChatRequest):
    if request.question.strip().lower() == "end":
        clear_history()
        return ChatResponse(answer = "Chat session ended")
            
    
    answer = ask_codebase(request.question)
    return ChatResponse(answer=answer)