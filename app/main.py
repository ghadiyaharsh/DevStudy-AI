from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from app.rag_module import load_and_store_pdf, rag_answer
from fastapi import UploadFile, File, Form
import shutil

from app.llm_service import generate_response
from fastapi import Form

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

@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    file_location = f"uploaded_{file.filename}"

    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    load_and_store_pdf(file_location)

    return RedirectResponse(url="/study", status_code=303)

@app.post("/ask-rag", response_class=HTMLResponse)
async def ask_rag(request: Request, question: str = Form(...)):
    answer = rag_answer(question)
    return templates.TemplateResponse(
        "study.html",
        {"request":request,"answer": answer}
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

1. Explain what the following code does.
2. Identify potential issues or bugs.
3. Suggest improvements if possible.

Code:
{code}
"""

    from app.llm_service import generate_response
    answer = generate_response(prompt)

    return templates.TemplateResponse(
        "code.html",
        {"request": request, "answer": answer}
    )