from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from database import supabase

app = FastAPI()

# Atenção: Se sua pasta estiver com 'T' maiúsculo no VS Code, deixe 'Templates' aqui
templates = Jinja2Templates(directory="Templates")

@app.get("/acougueiro", response_class=HTMLResponse)
async def painel_acougueiro(request: Request):
    # Busca estoque real do seu banco
    res = supabase.table('estoque').select("*").execute()
    estoque_real = res.data
    
    # Insights "fake" por enquanto (logo conectamos a IA real)
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
    