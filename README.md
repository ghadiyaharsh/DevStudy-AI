# DevStudy AI

DevStudy AI is an AI-powered study assistant that helps students learn from their PDF documents and understand programming code using AI.

The application uses Retrieval-Augmented Generation (RAG) to extract knowledge from uploaded PDFs and allows users to ask questions based on the document content. It also includes a Code Assistant that explains code and helps with debugging.

---

## 🚀 Features

### 📚 Study Assistant

* Upload PDF documents
* Automatically split documents into chunks
* Convert chunks into vector embeddings
* Store embeddings in a vector database
* Ask questions related to the uploaded document
* AI retrieves relevant context and generates answers

### 💻 Code Assistant

* Paste programming code
* AI explains the code logic
* AI suggests improvements or debugging tips

---

## 🧠 How It Works

### RAG Pipeline

1. User uploads a PDF
2. The document is split into smaller chunks
3. Chunks are converted into embeddings
4. Embeddings are stored in a vector database (ChromaDB)
5. When a user asks a question:

   * The question is converted to an embedding
   * Relevant chunks are retrieved
   * The AI model generates an answer based on that context

---

## 🛠 Tech Stack

Frontend:

* HTML
* CSS
* Jinja Templates

Backend:

* FastAPI

AI / ML:

* Ollama (Local LLM)
* LangChain
* HuggingFace Embeddings
* ChromaDB Vector Database

---

## 📂 Project Structure

```
DevStudy-AI
│
├── app
│   ├── main.py
│   ├── rag_module.py
│   ├── llm_service.py
│
├── templates
│   ├── base.html
│   ├── index.html
│   ├── study.html
│   └── code.html
│
├── static
│   └── style.css
│
├── uploads
├── chroma_db
├── tests
│
├── requirements.txt
└── README.md
```

---

## ⚙ Installation

Clone the repository:

```
git clone https://github.com/YOUR_USERNAME/DevStudy-AI.git
```

Move into project folder:

```
cd DevStudy-AI
```

Create virtual environment:

```
python -m venv my_env
```

Activate environment:

Windows:

```
my_env\Scripts\activate
```

Install dependencies:

```
pip install -r requirements.txt
```

---

## ▶ Running the Application

Start FastAPI server:

```
uvicorn app.main:app --reload
```

Open browser:

```
http://127.0.0.1:8000
```

---

## 📌 Future Improvements

* Support multiple PDF documents
* Improve UI design
* Add chat history
* Deploy the application online
* Add authentication for users

---

## 👨‍💻 Author

Created by Harsh Ghadiya

Computer Engineering Student | AI & Web Development Enthusiast
