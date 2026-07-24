from app.llm.service import ask_codebase


question = "Where is authentication implemented if it implemented? If no authentication then answer with no"

answer = ask_codebase(question)

print("\nANSWER:\n")
print(answer)