from app.retrieval.retriever import retriever


questions = [
    "Where is authentication implemented?",
    "What does the main application entry point do?",
    "How is the user interface structured?",
]


for question in questions:
    print("\n" + "=" * 100)
    print(f"QUESTION: {question}")
    print("=" * 100)

    documents = retriever.invoke(question)

    print(f"\nRetrieved {len(documents)} documents:\n")

    for i, document in enumerate(documents, start=1):
        print("-" * 100)
        print(f"RESULT {i}")
        print(f"FILE: {document.metadata.get('file_path')}")
        print("-" * 100)
        print(document.page_content[:1000])