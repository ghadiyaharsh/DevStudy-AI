from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from app.rag_module import load_and_store_pdf, rag_answer
from fastapi import UploadFile, File, Form
import os
import shutil

from app.llm_service import generate_response
from fastapi import Form
pdf_uploaded = False

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.post("/ask")
def ask_ai(question:str = Form(...)):
    answer = generate_response(question)
    return {"answer":answer}

from fastapi.responses import RedirectResponse

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.post("/upload-pdf")
async def upload_pdf(request: Request, file: UploadFile = File(...)):
    
    global pdf_uploaded
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # remove old vector database
    if os.path.exists("chroma_db"):
        shutil.rmtree("chroma_db")

    # process PDF for RAG
    load_and_store_pdf(file_path)

    pdf_uploaded = True

    return templates.TemplateResponse(
        "study.html",
        {
            "request": request,
            "message": "✅ PDF uploaded successfully!"
        }
    )

@app.post("/ask-rag", response_class=HTMLResponse)
async def ask_rag(request: Request, question: str = Form(...)):
    global pdf_uploaded

    if not pdf_uploaded:
        return templates.TemplateResponse(
            "study.html",
            {
                "request": request,
                "error": "⚠️ Please upload a PDF first."
            }
        )

    if not question.strip():
        return templates.TemplateResponse(
            "study.html",
            {
                "request": request,
                "error": "⚠️ Question cannot be empty."
            }
        )

    answer = rag_answer(question)

    return templates.TemplateResponse(
        "study.html",
        {
            "request": request,
            "answer": answer
        }
    ) 

@app.get("/study", response_class=HTMLResponse)
async def study_page(request: Request):
    return templates.TemplateResponse("study.html", {"request": request})

@app.get("/code", response_class=HTMLResponse)
async def code_page(request: Request):
    return templates.TemplateResponse("code.html", {"request": request})


@app.post("/explain-code", response_class=HTMLResponse)
async def explain_code(request: Request, code: str = Form(...)):
    prompt = f"""
You are an expert programming assistant.

Analyze the following code and respond in this format:

### Code Explanation
Explain what the code does clearly.

### Possible Issues
Mention bugs or bad practices if any.

### Suggested Improvements
Suggest improvements or optimizations.

Code:
{code}
"""

    from app.llm_service import generate_response
    answer = generate_response(prompt)

    return templates.TemplateResponse(
        "code.html",
        {"request": request, "answer": answer}
    )