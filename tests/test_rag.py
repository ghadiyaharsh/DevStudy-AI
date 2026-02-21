from app.rag_module import load_and_store_pdf, rag_answer, query_vectorstore

#1 Load PDF

print(load_and_store_pdf("think_python.pdf"))

#2 Ask Question

answer = rag_answer("understand python math functionp?")
print("\nFinal Answer:\n")
print(answer)