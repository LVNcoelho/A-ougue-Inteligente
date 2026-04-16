from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from database import supabase
import uvicorn

app = FastAPI()

# Forçando o diretório templates
templates = Jinja2Templates(directory="templates")

@app.get("/acougueiro", response_class=HTMLResponse)
async def painel_acougueiro(request: Request):
    try:
        # Tenta buscar os dados
        res = supabase.table('estoque').select("*").execute()
        estoque_real = res.data
        print(f"DEBUG - Dados do estoque: {estoque_real}") # Isso vai aparecer no terminal!
    except Exception as e:
        print(f"DEBUG - Erro no Supabase: {e}")
        estoque_real = []
    
    avisos_ia = [
        "A costelinha está com pouca saída hoje.",
        "Dica: O fim de semana está chegando, verifique o kit feijoada!"
    ]
    
    return templates.TemplateResponse("acougueiro.html", {
        "request": request, 
        "estoque": estoque_real,
        "avisos": avisos_ia
    })

@app.get("/cliente", response_class=HTMLResponse)
async def painel_cliente(request: Request):
    return templates.TemplateResponse("cliente.html", {"request": request})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)