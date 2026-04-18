from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from .database import supabase  
import os

app = FastAPI()

# Configuração de caminhos para os templates 
current_dir = os.path.dirname(os.path.realpath(__file__))
template_path = os.path.join(current_dir, "..", "templates")
templates = Jinja2Templates(directory=template_path)

# --- 0. ROTA RAIZ ---
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    # AJUSTE: Nomes explícitos para evitar erro de dicionário
    return templates.TemplateResponse(
        name="index.html", 
        context={"request": request}
    )

# --- 1. PAINEL DO AÇOUGUEIRO ---
@app.get("/acougueiro", response_class=HTMLResponse)
async def painel_acougueiro(request: Request):
    try:
        # Busca o estoque atual
        res_estoque = supabase.table('estoque').select("*").execute()
        estoque_real = res_estoque.data
        
        # Busca as últimas 5 vendas
        res_vendas = supabase.table('historico_pedidos').select("*").order('data_venda', desc=True).limit(5).execute()
        vendas_recentes = res_vendas.data
    except Exception as e:
        print(f"Erro ao carregar dados: {e}")
        estoque_real = []
        vendas_recentes = []
    
    return templates.TemplateResponse(
        name="acougueiro.html", 
        context={"request": request, "estoque": estoque_real, "vendas": vendas_recentes}
    )

# --- 2. CADASTRAR NOVA CARNE ---
@app.post("/adicionar_estoque")
async def adicionar_estoque(nome: str = Form(...), quantidade: float = Form(...), preco: float = Form(...)):
    try:
        supabase.table('estoque').insert({
            "nome": nome, 
            "quantidade": quantidade, 
            "preco_quilo": preco
        }).execute()
    except Exception as e:
        print(f"Erro ao inserir estoque: {e}")
    return RedirectResponse(url="/acougueiro", status_code=303)

# --- 3. REGISTRAR VENDA ---
@app.post("/registrar_venda")
async def registrar_venda(
    nome_cliente: str = Form(...), 
    whatsapp: str = Form(...), 
    carne_id: int = Form(...), 
    peso_vendido: float = Form(...)
):
    try:
        carne = supabase.table('estoque').select("*").eq('id', carne_id).single().execute()
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

    except Exception as e:
        print(f"Erro ao processar venda: {e}")
    
    return RedirectResponse(url="/acougueiro", status_code=303)

# --- 4. ESTRATÉGIAS DE VENDA (INSIGHTS) ---
@app.get("/gerar_insights")
async def gerar_insights():
    try:
        res = supabase.table('estoque').select("*").execute()
        estoque = res.data
        insights = []
        
        for item in estoque:
            nome = item['nome'].lower()
            qtd = float(item['quantidade'])
            
            if 'frango' in nome and qtd > 20:
                insights.append("Mano, o frango tá muito alto e a temperatura de Castanhal vai subir, faz uma promoção de espetinho!!")
            
            if qtd < 5:
                insights.append(f"Cuidado! O estoque de {item['nome']} está acabando. Melhor repor!")

        if not insights:
            insights = ["O estoque está equilibrado. Bom trabalho!"]
            
        return {"avisos": insights}
    except Exception as e:
        return {"avisos": [f"Erro na IA: {e}"]}

# --- 5. PAINEL DO CLIENTE (CATÁLOGO) ---
@app.get("/cliente", response_class=HTMLResponse)
async def painel_cliente(request: Request):
    try:
        res = supabase.table('estoque').select("*").execute()
        # AJUSTE: Nomes explícitos para garantir o deploy no Render
        return templates.TemplateResponse(
            name="cliente.html", 
            context={"request": request, "estoque": res.data}
        )
    except Exception as e:
        return HTMLResponse(content=f"Erro ao carregar catálogo: {e}", status_code=500)

app = app
