
from fastapi import FastAPI, Request, Form
from fastapi.responses import JSONResponse
from database import supabase 
import os

app = FastAPI()

# --- 1. BUSCAR DADOS (ESTOQUE E VENDAS) ---
# Esta rota é chamada pelo useEffect do seu App.tsx
@app.get("/api/acougueiro")
async def painel_acougueiro():
    try:
        # Busca estoque real do Supabase
        res_estoque = supabase.table('estoque').select("*").execute()
        estoque_real = res_estoque.data
        
        # Busca as últimas 5 vendas para o histórico
        res_vendas = supabase.table('historico_pedidos').select("*").order('data_venda', desc=True).limit(5).execute()
        vendas_recentes = res_vendas.data
        
        # Retorna JSON puro para o React
        return {
            "estoque": estoque_real, 
            "vendas": vendas_recentes
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
        # Busca info da carne para cálculo
        carne = supabase.table('estoque').select("*").eq('id', carne_id).single().execute()
        if not carne.data:
            return JSONResponse(status_code=404, content={"erro": "Carne não encontrada"})
            
        nome_carne = carne.data['nome']
        preco_total = carne.data['preco_quilo'] * peso_vendido

        # Insere no histórico de vendas
        supabase.table('historico_pedidos').insert({
            "cliente_nome": nome_cliente,
            "cliente_whatsapp": whatsapp,
            "itens_comprados": f"{peso_vendido}kg de {nome_carne}",
            "valor_total": preco_total
        }).execute()

        # Atualiza a quantidade no estoque
        nova_qtd = carne.data['quantidade'] - peso_vendido
        supabase.table('estoque').update({"quantidade": nova_qtd}).eq('id', carne_id).execute()
        
        return {"mensagem": "Venda registrada!", "valor_total": preco_total}
    except Exception as e:
        return JSONResponse(status_code=500, content={"erro": str(e)})

# --- 4. ESTRATÉGIAS DE VENDA (INSIGHTS) ---
@app.get("/api/gerar_insights")
async def gerar_insights():
    try:
        res = supabase.table('estoque').select("*").execute()
        estoque = res.data
        insights = []
        
        for item in estoque:
            nome = item['nome'].lower()
            qtd = float(item['quantidade'])
            
            # Lógica personalizada para a região
            if 'frango' in nome and qtd > 20:
                insights.append("Mano, o frango tá com estoque alto e o calor em Castanhal tá pedindo um espetinho na orla!")
            
            if qtd < 5:
                insights.append(f"Atenção: O estoque de {item['nome']} está no fim. Hora de repor!")

        if not insights:
            insights = ["O balcão está equilibrado. Bora vender!"]
            
        return {"avisos": insights}
    except Exception as e:
        return {"avisos": [f"Erro na IA: {e}"]}

# --- 5. ROTA DE STATUS ---
@app.get("/api/status")
async def status():
    return {"status": "Online", "projeto": "Açougue Inteligente Mercadão das Carnes!"}