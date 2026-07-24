from app.llm.service import ask_codebase


question = "Where is authentication implemented if it implemented?"

answer = ask_codebase(question)

print("\nANSWER:\n")
print(answer)