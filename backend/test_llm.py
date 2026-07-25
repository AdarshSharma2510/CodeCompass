from app.llm.service import ask_codebase

questions = [
    "Where is the Kanban board implemented?",
    "How is the user interface structured?",
    "Where is authentication implemented?",
]

for question in questions:
    print("\n" + "=" * 100)
    print("QUESTION:", question)
    print("=" * 100)

    answer = ask_codebase(question)

    print("\nANSWER:\n")
    print(answer)