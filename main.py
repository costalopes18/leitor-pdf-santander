from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import fitz  # PyMuPDF: Biblioteca ultra-rápida para ler PDFs digitais
import base64

app = FastAPI()

# Modelo de dados que o Google Apps Script vai enviar
class PDFRequest(BaseModel):
    filename: str
    file_base64: str

@app.post("/extract-text")
def extract_text(request: PDFRequest):
    try:
        # 1. Decodifica o arquivo enviado pelo Google Apps Script
        pdf_bytes = base64.b64decode(request.file_base64)
        
        # 2. Abre o PDF na memória
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        
        texto_completo = ""
        
        # 3. Extrai o texto puro de cada página (sem problemas de espaços nas taxas)
        for page in doc:
            texto_completo += page.get_text("text") + "\n"
            
        doc.close()
        
        return {"status": "success", "text": texto_completo}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar PDF: {str(e)}")

# Para testar localmente: uvicorn main:app --reload
