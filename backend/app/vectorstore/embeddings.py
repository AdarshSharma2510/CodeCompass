from langchain_huggingface import HuggingFaceEmbeddings, HuggingFaceEndpoint
from app.config.settings import settings

embeddings = HuggingFaceEmbeddings(
    model_name=settings.EMBEDDING_MODEL,
    model_kwargs={
        "device": "cpu"
    },
    encode_kwargs={
        "normalize_embeddings": True
    },
    
)