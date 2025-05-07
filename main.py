from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import pdfplumber
import io

app = FastAPI()

# Enable CORS if you're calling this from a Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace * with your Next.js domain in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/extract-text/")
async def extract_text(file: UploadFile = File(...)):
    content = await file.read()
    text_by_page = []

    with pdfplumber.open(io.BytesIO(content)) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            text_by_page.append({
                "page": i + 1,
                "text": text
            })

    return {"filename": file.filename, "pages": text_by_page}
