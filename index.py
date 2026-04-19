from fastapi import FastAPI, Request, Form
from fastapi.responses import JSONResponse
import os
import os
from dotenv import load_dotenv

if not os.getenv("VERCEL"):
    load_dotenv()
from database import supabase 

app = FastAPI()

# --- 1. BUSCAR DADOS (ESTOQUE E VENDAS) ---
@app.get("/api/acougueiro")
async def painel_acougueiro():
    try:
        res_estoque = supabase.table('estoque').select("*").execute()
        res_vendas = supabase.table('historico_pedidos').select("*").order('data_venda', desc=True).limit(5).execute()
        
        return {
            "estoque": res_estoque.data, 
            "vendas": res_vendas.data
        }
    except Exception as e:
        return JSONResponse(
            status_code=500, 
            content={"erro": f"Erro ao carregar dados: {str(e)}", "estoque": [], "vendas": []}
        )

# --- 2. CADASTRAR NOVA CARNE ---
@app.post("/api/adicionar_estoque")
async def adicionar_estoque(nome: str = Form(...), quantidade: float = Form(...), preco: float = Form(...)):
    try:
        supabase.table('estoque').insert({
            "nome": nome, 
            "quantidade": quantidade, 
            "preco_quilo": preco
        }).execute()
        return {"mensagem": "Estoque atualizado com sucesso!"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"erro": str(e)})

# --- 3. REGISTRAR VENDA ---
@app.post("/api/registrar_venda")
async def registrar_venda(
    nome_cliente: str = Form(...), 
    whatsapp: str = Form(...), 
    carne_id: int = Form(...), 
    peso_vendido: float = Form(...)
):
    try:
        carne = supabase.table('estoque').select("*").eq('id', carne_id).single().execute()
        if not carne.data:
            return JSONResponse(status_code=404, content={"erro": "Carne não encontrada"})
            
        nome_carne = carne.data['nome']
        preco_total = carne.data['preco_quilo'] * peso_vendido

        supabase.table('historico_pedidos').insert({
            "cliente_nome": nome_cliente,
            "cliente_whatsapp": whatsapp,
            "itens_comprados": f"{peso_vendido}kg de {nome_carne}",
            "valor_total": preco_total
        }).execute()

        nova_qtd = carne.data['quantidade'] - peso_vendido
        supabase.table('estoque').update({"quantidade": nova_qtd}).eq('id', carne_id).execute()
        
        return {"mensagem": "Venda registrada!", "valor_total": preco_total}
    except Exception as e:
        return JSONResponse(status_code=500, content={"erro": str(e)})

# --- 4. ROTA DE STATUS ---
@app.get("/api/status")
async def status():
    return {"status": "Online", "projeto": "Açougue Inteligente Mercadão das Carnes!"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)