from app.llm.service import ask_codebase


question = "tell me in what file is it used. also specify what is the 'it' I am referring to" 

answer = ask_codebase(question)

print("\nANSWER:\n")
print(answer)