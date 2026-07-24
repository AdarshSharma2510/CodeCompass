from fastapi import APIRouter
from pydantic import BaseModel

from app.llm.service import ask_codebase


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
    answer = ask_codebase(request.question)

    return ChatResponse(answer=answer)