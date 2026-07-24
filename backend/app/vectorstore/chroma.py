from pathlib import Path

from langchain_chroma import Chroma

from app.config.settings import settings
from app.vectorstore.embeddings import embeddings


# print("Current working directory:", Path.cwd())
# print("Chroma path:", settings.CHROMA_DB_PATH)
# print(
#     "Absolute Chroma path:",
#     Path(settings.CHROMA_DB_PATH).resolve(),
# )


vector_store = Chroma(
    collection_name="repository",
    embedding_function=embeddings,
    persist_directory=settings.CHROMA_DB_PATH,
)