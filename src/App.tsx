import React, { useState, useEffect } from 'react';
import { 
  LayoutDashboard, 
  ShoppingCart, 
  Beef, 
  BrainCircuit, 
  PlusCircle, 
  History,
  TrendingUp
} from 'lucide-react';

const App: React.FC = () => {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [estoque, setEstoque] = useState<any[]>([]); 
  const [vendas, setVendas] = useState<any[]>([]);
  const [insights, setInsights] = useState<string[]>([]);
  const [loadingIA, setLoadingIA] = useState(false);
  const [loadingDados, setLoadingDados] = useState(true);

  // Link oficial da API no Codespaces
  const API_URL = "https://congenial-telegram-pjw6jjqjgxrjc5wj-8000.app.github.dev";

  // 1. BUSCAR DADOS DO CSV (VIA BACKEND PYTHON)
  const fetchData = async () => {
    setLoadingDados(true);
    try {
      const res = await fetch(`${API_URL}/api/acougueiro`);
      const data = await res.json();
      
      if (data.status === "sucesso") {
        setEstoque(data.estoque);
        setVendas(data.vendas || []);
        console.log("Estoque do Mercadão carregado com sucesso!");
      }
    } catch (err) {
      console.error("Erro ao conectar na API:", err);
      // Dados de fallback caso o Codespaces esteja offline
      setEstoque([
        { corte: 'Músculo (Offline)', kg: 0, preco_quilo: 0, validade: '-' },
      ]);
    }
    setLoadingDados(false);
  };

  useEffect(() => {
    fetchData();
  }, []);

  // 2. GERAR INSIGHTS IA (CONECTA TI + GEMINI)
  const gerarInsights = async () => {
    setLoadingIA(true);
    
    const payload = {
      "data_atual": "21/04/2026",
      "itens_estoque": estoque.map(item => ({
        "corte": item.corte,
        "kg": item.kg,
        "validade": item.validade || "Não informada"
      }))
    };

    try {
      const res = await fetch(`${API_URL}/agente/balcao`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      const data = await res.json();
      
      if (data.status === "sucesso") {
        setInsights([data.insights]);
      } else {
        setInsights(["IA: Verifique se o arquivo estoque.csv possui dados válidos."]);
      }
    } catch (err) {
      setInsights(["Erro: O servidor do Codespaces não respondeu. Verifique a porta 8000!"]);
    }
    setLoadingIA(false);
  };

  return (
    <div className="flex min-h-screen bg-gray-50 font-sans text-gray-900">
      {/* SIDEBAR */}
      <aside className="w-72 bg-white border-r border-gray-200 flex flex-col fixed h-full shadow-xl z-10">
        <div className="p-8 flex items-center gap-3">
          <div className="bg-red-600 p-2 rounded-2xl shadow-lg shadow-red-100 text-white">
            <Beef size={32} />
          </div>
          <div>
            <h1 className="text-xl font-black text-gray-800 leading-none uppercase">Açougue</h1>
            <span className="text-[10px] font-bold text-red-500 tracking-[0.2em] uppercase">Inteligente SJP</span>
          </div>
        </div>

        <nav className="flex-1 px-4 space-y-2">
          <button 
            onClick={() => setActiveTab('dashboard')}
            className={`w-full flex items-center gap-4 px-4 py-4 rounded-2xl font-bold transition-all ${activeTab === 'dashboard' ? 'bg-red-50 text-red-600' : 'text-gray-400 hover:bg-gray-50'}`}
          >
            <LayoutDashboard size={22} /> Painel Geral
          </button>
          <button 
            onClick={() => setActiveTab('vendas')}
            className={`w-full flex items-center gap-4 px-4 py-4 rounded-2xl font-bold transition-all ${activeTab === 'vendas' ? 'bg-red-50 text-red-600' : 'text-gray-400 hover:bg-gray-50'}`}
          >
            <ShoppingCart size={22} /> Registrar Venda
          </button>
          <button 
            onClick={() => setActiveTab('estoque')}
            className={`w-full flex items-center gap-4 px-4 py-4 rounded-2xl font-bold transition-all ${activeTab === 'estoque' ? 'bg-red-50 text-red-600' : 'text-gray-400 hover:bg-gray-50'}`}
          >
            <PlusCircle size={22} /> Abastecer
          </button>
        </nav>

        <div className="p-6">
          <button 
            onClick={gerarInsights}
            disabled={loadingIA || loadingDados}
            className="w-full bg-gradient-to-br from-amber-400 to-orange-500 text-white p-4 rounded-3xl font-black flex items-center justify-center gap-2 shadow-lg shadow-orange-100 hover:scale-105 transition-transform disabled:opacity-50"
          >
            <BrainCircuit size={20} />
            {loadingIA ? 'ANALISANDO...' : 'IA INSIGHTS'}
          </button>
        </div>
      </aside>

      {/* CONTEÚDO PRINCIPAL */}
      <main className="flex-1 ml-72 p-12">
        <div className="max-w-5xl mx-auto">
          
          {/* ÁREA DE INSIGHTS DA IA */}
          {insights.length > 0 && (
            <div className="mb-8 bg-amber-50 border-2 border-amber-200 p-6 rounded-[32px] flex items-start gap-4 animate-bounce-subtle">
              <div className="bg-amber-400 p-2 rounded-xl text-white">
                <BrainCircuit size={24} />
              </div>
              <div className="flex-1">
                <h4 className="font-black text-amber-800 uppercase text-xs tracking-wider mb-2">Estratégia de Venda - IA Conecta TI</h4>
                {insights.map((txt, i) => (
                  <p key={i} className="text-amber-900 font-bold whitespace-pre-wrap leading-relaxed">
                    {txt}
                  </p>
                ))}
              </div>
              <button onClick={() => setInsights([])} className="text-amber-400 hover:text-amber-600 font-black">✕</button>
            </div>
          )}

          {activeTab === 'dashboard' && (
            <div className="space-y-10">
              <header className="flex justify-between items-end">
                <div>
                  <h2 className="text-4xl font-black text-gray-800">Status do Balcão</h2>
                  <p className="text-gray-400 font-medium tracking-tight">Estoque local: São João da Ponta/PA</p>
                </div>
                <div className="bg-white p-4 rounded-3xl shadow-sm border border-gray-100 flex items-center gap-4">
                  <div className="bg-green-100 p-2 rounded-xl text-green-600"><TrendingUp size={24} /></div>
                  <div>
                    <p className="text-[10px] font-black text-gray-400 uppercase tracking-widest">Meta do Dia</p>
                    <p className="text-xl font-black text-gray-800">R$ 1.250,00</p>
                  </div>
                </div>
              </header>

              {/* GRID DE CARNES (Vem do CSV) */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {loadingDados ? (
                  <div className="col-span-3 text-center py-20">
                    <div className="animate-spin inline-block w-8 h-8 border-4 border-red-600 border-t-transparent rounded-full mb-4"></div>
                    <p className="text-gray-400 font-black uppercase tracking-tighter">Sincronizando com o Balcão SJP...</p>
                  </div>
                ) : estoque.length > 0 ? (
                  estoque.map((item: any, index: number) => (
                    <div key={index} className="bg-white p-8 rounded-[40px] shadow-sm border border-gray-100 hover:shadow-2xl hover:-translate-y-1 transition-all group">
                      <div className="flex justify-between items-start mb-6">
                        <div className="bg-gray-50 p-3 rounded-2xl group-hover:bg-red-600 group-hover:text-white transition-colors">
                          <Beef size={28} />
                        </div>
                        <span className={`px-4 py-1 rounded-full text-[10px] font-black uppercase ${item.kg < 10 ? 'bg-red-100 text-red-600 animate-pulse' : 'bg-green-100 text-green-600'}`}>
                          {item.kg < 10 ? 'Repor' : 'Ok'}
                        </span>
                      </div>
                      <h3 className="text-xl font-black text-gray-800 uppercase mb-1 truncate">{item.corte}</h3>
                      <div className="flex items-baseline gap-1">
                        <span className="text-3xl font-black text-gray-800">{item.kg}</span>
                        <span className="text-gray-400 font-bold uppercase text-[10px]">Kg disponíveis</span>
                      </div>
                      <p className="mt-4 text-green-600 font-black text-lg">R$ {parseFloat(item.preco_quilo).toFixed(2)}/kg</p>
                    </div>
                  ))
                ) : (
                  <div className="col-span-3 text-center py-10 text-gray-400 font-bold">Arquivo estoque.csv não encontrado.</div>
                )}
              </div>

              {/* HISTÓRICO */}
              <div className="bg-white rounded-[40px] p-8 shadow-sm border border-gray-100">
                <h3 className="text-2xl font-black text-gray-800 mb-6 flex items-center gap-3">
                  <History className="text-gray-400" /> Vendas Recentes
                </h3>
                <div className="space-y-4">
                  {vendas.length > 0 ? (
                    vendas.map((v: any, i: number) => (
                      <div key={i} className="flex justify-between items-center p-4 hover:bg-gray-50 rounded-2xl transition-colors border-b border-gray-50 last:border-0">
                        <div>
                          <p className="font-black text-gray-800">{v.cliente_nome}</p>
                          <p className="text-xs text-gray-400 font-bold uppercase">{v.itens_comprados}</p>
                        </div>
                        <div className="text-right">
                          <p className="font-black text-red-600">R$ {v.valor_total}</p>
                          <p className="text-[10px] text-gray-300 font-bold uppercase tracking-widest">Pago via PIX</p>
                        </div>
                      </div>
                    ))
                  ) : (
                    <p className="text-center text-gray-400 font-bold">Pronto para a primeira venda do dia!</p>
                  )}
                </div>
              </div>
            </div>
          )}

          {activeTab === 'vendas' && <div className="text-center py-20 font-black text-gray-300 text-4xl uppercase opacity-20">PDV Offline</div>}
          {activeTab === 'estoque' && <div className="text-center py-20 font-black text-gray-300 text-4xl uppercase opacity-20">Logística SJP</div>}
          
        </div>
      </main>
    </div>
  );
};

export default App;