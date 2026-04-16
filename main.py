from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from database import supabase
import uvicorn

app = FastAPI()

# Note o "templates" em minúsculo para bater com sua pasta
templates = Jinja2Templates(directory="templates")

@app.get("/acougueiro", response_class=HTMLResponse)
async def painel_acougueiro(request: Request):
    try:
        # Busca estoque real do seu banco
        res = supabase.table('estoque').select("*").execute()
        estoque_real = res.data
    except Exception as e:
        print(f"Erro no banco: {e}")
        estoque_real = []
    
    # Insights simulados
    avisos_ia = [
        "A costelinha está com pouca saída hoje.",
        "Dica: O fim de semana está chegando, verifique o kit feijoada!"
    ]
    
    return templates.TemplateResponse(
        request=request, 
        name="acougueiro.html", 
        context={
            "estoque": estoque_real,
            "avisos": avisos_ia
        }
    )

@app.get("/cliente", response_class=HTMLResponse)
async def painel_cliente(request: Request):
    return templates.TemplateResponse(
        request=request, 
        name="cliente.html", 
        context={}
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)