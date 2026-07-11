from langchain_huggingface import HuggingFaceEmbeddings

from app.config.settings import settings

embeddings = HuggingFaceEmbeddings(
    model_name=settings.EMBEDDING_MODEL,
    model_kwargs={"device": "gpu"},
    encode_kwargs={"normalize_embeddings": True},
)