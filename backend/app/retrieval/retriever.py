from app.vectorstore.chroma import vector_store


retriever = vector_store.as_retriever(
    search_type="similarity",
    search_kwargs={
        "k": 5,
    },
)
