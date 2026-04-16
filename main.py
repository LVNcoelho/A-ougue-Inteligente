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

@app.get("/gerar_insights")
async def gerar_insights():
    try:
        # 1. Pega o estoque atual do banco
        res = supabase.table('estoque').select("*").execute()
        estoque = res.data
        
        # 2. Lógica da IA 
        insights = []
        for item in estoque:
            if 'frango' in item['nome'].lower() and item['quantidade'] > 20:
                insights.append("Mano, o frango tá muito alto e a temperatura de Castanhal vai subir, faz uma promoção de espetinho!!")
            
            if item['quantidade'] < 5:
                insights.append(f"Cuidado! O estoque de {item['nome']} está acabando. Melhor repor!")

        if not insights:
            insights = ["O estoque está equilibrado. Bom trabalho!"]

        # 3. Retorna os avisos para o painel
        return {"avisos": insights}
        
    except Exception as e:
        return {"avisos": [f"Erro ao consultar a IA: {e}"]}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
