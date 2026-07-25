from langchain_core.documents import Document
from flashrank import Ranker, RerankRequest

from app.vectorstore.chroma import vector_store


ranker = Ranker(
    model_name="ms-marco-MiniLM-L-12-v2",
    cache_dir="data/flashrank",
)


def retrieve_and_rerank(
    query: str,
    initial_k: int = 25,
    final_k: int = 8,
) -> list[Document]:
    documents = vector_store.similarity_search(query, k=initial_k)

    passages = [
        {
            "id": str(i),
            "text": doc.page_content,
            "meta": doc.metadata,
        }
        for i, doc in enumerate(documents)
    ]

    rerank_request = RerankRequest(
        query=query,
        passages=passages,
    )

    results = ranker.rerank(rerank_request)

    reranked_documents = []
    for result in results[:final_k]:
        meta = result.get("meta", {})
        reranked_documents.append(
            Document(
                page_content=result.get("text", ""),
                metadata=meta,
            )
        )

    return reranked_documents