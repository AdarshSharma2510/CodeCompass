from langchain_chroma import Chroma

from app.config.settings import settings
from app.vectorstore.embeddings import embeddings


vector_store = Chroma(
    collection_name="repository",
    embedding_function=embeddings,
    persist_directory=settings.CHROMA_DB_PATH,
)