from app.vectorstore.chroma import vector_store


print("Collection:", vector_store._collection.name)
print("Count:", vector_store._collection.count())