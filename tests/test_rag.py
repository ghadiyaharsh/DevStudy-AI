from app.rag_module import load_and_store_pdf, query_vectorstore

#1 Load PDF

print(load_and_store_pdf("sample.pdf"))

#2 Ask Question

results = query_vectorstore("who write Python?")
for doc in results:
    print(doc.page_content)