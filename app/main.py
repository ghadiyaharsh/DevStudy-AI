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
    return templates.TemplateResponse("index.html", {"request": request})

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

    return RedirectResponse(url="/", status_code=303)

@app.post("/ask-rag")
async def ask_rag(question: str = Form(...)):
    answer = rag_answer(question)
    return {"answer": answer}