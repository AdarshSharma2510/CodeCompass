from langchain_core.documents import Document

from app.vectorstore.chroma import vector_store


class RepositoryIndexer:
    def index(self, documents: list[Document]) -> None:
        print(f"Documents received by indexer: {len(documents)}")

        vector_store.reset_collection()

        print(
            "Collection count after reset:",
            vector_store._collection.count(),
        )

        vector_store.add_documents(documents)

        print(
            "Collection count after indexing:",
            vector_store._collection.count(),
        )