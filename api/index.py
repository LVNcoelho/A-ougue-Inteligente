import os
from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client
from httpx import SyncHTTPTransport 

# CONFIGURAÇÃO DE ELITE PARA VERCEL
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

supabase = create_client(url, key)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1. PEGAR AS VARIÁVEIS (Direto do ambiente do Vercel)
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

# 2. CRIAR O CLIENTE APENAS UMA VEZ
if not url or not key:
    raise RuntimeError("Faltam as chaves do Supabase no painel do Vercel!")

supabase = create_client(url, key)

app = FastAPI()
# ... resto do seu código das rotas abaixo ...

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/estoque")
async def listar_estoque():
    # Sem try/except gigante para o log nos mostrar o erro real se falhar
    res = supabase.table('estoque').select("*").execute()
    return res.data

@app.get("/api/vendas")
async def listar_vendas():
    res = supabase.table('historico_pedidos').select("*").order('data_venda', desc=True).limit(5).execute()
    return res.data

@app.post("/adicionar_estoque")
async def adicionar_estoque(nome: str = Form(...), quantidade: float = Form(...), preco: float = Form(...)):
    supabase.table('estoque').insert({
        "nome": nome, "quantidade": quantidade, "preco_quilo": preco
    }).execute()
    return {"status": "ok"}

@app.post("/registrar_venda")
async def registrar_venda(nome_cliente: str = Form(...), whatsapp: str = Form(...), carne_id: int = Form(...), peso_vendido: float = Form(...)):
    carne = supabase.table('estoque').select("*").eq('id', carne_id).single().execute()
    preco_total = float(carne.data['preco_quilo']) * float(peso_vendido)
    
    supabase.table('historico_pedidos').insert({
        "cliente_nome": nome_cliente, "cliente_whatsapp": whatsapp,
        "itens_comprados": f"{peso_vendido}kg de {carne.data['nome']}", "valor_total": preco_total
    }).execute()

    nova_qtd = float(carne.data['quantidade']) - float(peso_vendido)
    supabase.table('estoque').update({"quantidade": nova_qtd}).eq('id', carne_id).execute()
    return {"status": "ok"}

@app.get("/gerar_insights")
async def gerar_insights():
    res = supabase.table('estoque').select("*").execute()
    insights = [f"Opa! {i['nome']} tá acabando!" for i in res.data if float(i['quantidade']) < 5]
    return {"avisos": insights or ["Estoque equilibrado no Mercadão das Carnes!"]}
