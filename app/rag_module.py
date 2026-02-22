from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from app.llm_service import generate_response

def load_and_store_pdf(pdf_path: str):
    # Load PDF
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    print("Total pages loaded:", len(documents))

    # Split into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = text_splitter.split_documents(documents)

    # Remove empty chunks
    chunks = [chunk for chunk in chunks if chunk.page_content.strip() != ""]

    print("Total valid chunks:", len(chunks))

    if not chunks:
        raise ValueError("No valid text chunks found in PDF.")

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-mpnet-base-v2"
    )

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory="chroma_db"
    )

    return "PDF processed and stored successfully."




def query_vectorstore(question:str):
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-mpnet-base-v2"
    )
    
    vectorstore = Chroma(
        persist_directory="chroma_db",
        embedding_function=embeddings
           
    )
    
    retriever = vectorstore.as_retriever(search_kwargs={"k":3})
    results = retriever.invoke(question)

    
    return results
    
    
    
def rag_answer(question:str):
    #1 retrieve relevent chunks
    results = query_vectorstore(question)
    
    if not results:
        return "The provided context does not contain enough information to answer this question."
    
    #2 merge context
    context = ""
    for doc in results:
        context += doc.page_content + "\n\n"
        
    #3 Create grounded prompt
    prompt = f"""
    Use the following context to answer the question.
    If the answer is not in the context, say you don't know.
    
    Context:
    {context}
    
    Question:
    {question}
    
    Answer:
    """
    
    #4 send to Ollama
    answer = generate_response(prompt)
    
    return answer      