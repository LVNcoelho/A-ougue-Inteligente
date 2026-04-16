from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from database import supabase
import uvicorn

app = FastAPI()

# Configuração dos templates
templates = Jinja2Templates(directory="templates")

@app.get("/acougueiro", response_class=HTMLResponse)
async def painel_acougueiro(request: Request):
    try:
        res = supabase.table('estoque').select("*").execute()
        estoque_real = res.data
    except Exception as e:
        print(f"Erro no banco: {e}")
        estoque_real = []
    
    avisos_ia = [
        "A costelinha está com pouca saída hoje.",
        "Dica: O fim de semana está chegando, verifique o kit feijoada!"
    ]
    
    return templates.TemplateResponse(
        request=request, 
        name="acougueiro.html", 
        context={"estoque": estoque_real, "avisos": avisos_ia}
    )

@app.post("/adicionar_estoque")
async def adicionar_estoque(nome: str = Form(...), quantidade: float = Form(...), preco: float = Form(...)):
    # Envia para o Supabase
    supabase.table('estoque').insert({
        "nome": nome, 
        "quantidade": quantidade, 
        "preco_quilo": preco
    }).execute()
    
    # Redireciona de volta para a página do açougueiro
    return RedirectResponse(url="/acougueiro", status_code=303)

@app.get("/cliente", response_class=HTMLResponse)
async def painel_cliente(request: Request):
    # Busca dados para o cliente também
    res = supabase.table('estoque').select("*").execute()
    estoque_real = res.data
    
    return templates.TemplateResponse(
        request=request, 
        name="cliente.html", 
        context={"estoque": estoque_real}
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)