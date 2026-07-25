from app.retrieval.retriever import retrieve_and_rerank


question = "Where is authentication implemented?"

documents = retrieve_and_rerank(question)

print(f"\nRetrieved {len(documents)} documents:\n")

for i, document in enumerate(documents, start=1):
    print("=" * 80)
    print(f"RESULT {i}")
    print(f"FILE: {document.metadata.get('file_path')}")
    print("=" * 80)
    print(document.page_content[:1000])
    print()