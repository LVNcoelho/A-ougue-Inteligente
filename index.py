from fastapi import FastAPI, Request, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Carregar variáveis de ambiente
if not os.getenv("VERCEL"):
    load_dotenv()

from database import supabase 

# Configuração do Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-pro")

app = FastAPI()

# Middleware de CORS para permitir que a Vercel acesse o Codespaces
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos de Dados para a IA
class ItemEstoque(BaseModel):
    corte: str
    kg: float
    validade: str

class DadosBalcao(BaseModel):
    data_atual: str
    itens_estoque: List[ItemEstoque]

# --- 1. BUSCAR DADOS (ESTOQUE E VENDAS) ---
@app.get("/api/acougueiro")
async def get_estoque():
    try:
        
        df = pd.read_csv('estoque.csv')
        estoque_lista = df.to_dict(orient='records')
        
        return {
            "status": "sucesso",
            "estoque": estoque_lista,
            "vendas": [
                {"id": 1, "cliente_nome": "Cliente Teste SJP", "itens_comprados": "2kg Picanha", "valor_total": "130.00"}
            ]
        }
    except Exception as e:
        return {"status": "erro", "mensagem": "Erro ao ler estoque local"}
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

# --- 4. ROTA DA IA (AGENTE DE BALCÃO) ---
@app.post("/agente/balcao")
async def agente_balcao(dados: DadosBalcao):
    try:
        # Montar o prompt para o Gemini
        prompt = f"""
        Você é o Consultor Estratégico do 'Açougue Inteligente SJP'.
        Data de hoje: {dados.data_atual}
        
        Estoque atual:
        {dados.itens_estoque}
        
        Sua tarefa:
        1. Analise produtos com validade próxima ou estoque muito alto.
        2. Crie uma oferta irresistível para o WhatsApp.
        3. Dê uma dica de gestão para o dono do açougue.
        
        Seja breve, use emojis e foco no lucro e evitar desperdício.
        """
        
        response = model.generate_content(prompt)
        return {"status": "sucesso", "insights": response.text}
    except Exception as e:
        return {"status": "erro", "detalhe": str(e)}

# --- 5. ROTA DE STATUS ---
@app.get("/api/status")
async def status():
    return {"status": "Online", "projeto": "Açougue Inteligente Mercadão das Carnes!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
