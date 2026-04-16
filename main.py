from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from database import supabase

app = FastAPI()


templates = Jinja2Templates(directory="Templates")

@app.get("/acougueiro", response_class=HTMLResponse)
async def painel_acougueiro(request: Request):
    # Busca estoque real do seu banco no Supabase
    try:
        res = supabase.table('estoque').select("*").execute()
        estoque_real = res.data
    except Exception as e:
        print(f"Erro ao buscar banco: {e}")
        estoque_real = []
    
    # Mensagens da IA (Simuladas)
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
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)