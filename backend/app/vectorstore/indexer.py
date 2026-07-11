from langchain_core.documents import Document

from app.vectorstore.chroma import vector_store


class RepositoryIndexer:
    def index(self, documents: list[Document]) -> None:
        vector_store.reset_collection()
        vector_store.add_documents(documents)
        