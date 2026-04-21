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
  const [estoque, setEstoque] = useState([
    // Exemplo de dados iniciais para a demonstração não abrir vazia
    { id: 1, nome: 'Músculo', quantidade: 10, preco_quilo: 28.90, validade: '22/04/2026' },
    { id: 2, nome: 'Patinho', quantidade: 5, preco_quilo: 35.00, validade: '24/04/2026' },
    { id: 3, nome: 'Acém', quantidade: 15, preco_quilo: 25.50, validade: '30/04/2026' }
  ]);
  const [vendas, setVendas] = useState([
    { id: 1, cliente_nome: 'João Silva', itens_comprados: '2kg Picanha', valor_total: '140,00', cliente_whatsapp: '91988776655' }
  ]);
  const [insights, setInsights] = useState<string[]>([]);
  const [loadingIA, setLoadingIA] = useState(false);

  // 1. BUSCAR DADOS (Simulado ou Real)
  const fetchData = async () => {
    try {
      // Quando seu banco estiver pronto, aponte para: 
      // const res = await fetch('https://fictional-bassoon-696954xrg9vcxxr-8000.app.github.dev/api/acougueiro');
      // const data = await res.json();
      // setEstoque(data.estoque || []);
      // setVendas(data.vendas || []);
      console.log("Dados carregados com sucesso.");
    } catch (err) {
      console.error("Erro ao carregar dados:", err);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  // 2. GERAR INSIGHTS IA (A Mágica da Conecta TI)
  const gerarInsights = async () => {
    setLoadingIA(true);
    
    // Link direto da sua API no Codespaces (removendo o /docs)
    const API_URL = "https://fictional-bassoon-696954xrg9vcxxr-8000.app.github.dev";

    // Pegamos os dados que estão no estado do React para enviar para o Gemini
    const payload = {
      "data_atual": "21/04/2026",
      "itens_estoque": estoque.map(item => ({
        "corte": item.nome,
        "kg": item.quantidade,
        "validade": item.validade
      }))
    };

    try {
      const res = await fetch(`${API_URL}/agente/balcao`, {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json' 
        },
        body: JSON.stringify(payload)
      });

      const data = await res.json();
      
      if (data.status === "sucesso") {
        // Colocamos o insight dentro do array para renderizar no seu card amarelo
        setInsights([data.insights]);
      } else {
        setInsights(["A IA encontrou um problema ao analisar o estoque. Verifique os dados."]);
      }
    } catch (err) {
      console.error("Erro na conexão:", err);
      setInsights(["Erro: Certifique-se que o Codespaces está rodando e a porta 8000 está Pública."]);
    }
    setLoadingIA(false);
  };

  return (
    <div className="flex min-h-screen bg-gray-50 font-sans">
      {/* SIDEBAR */}
      <aside className="w-72 bg-white border-r border-gray-200 flex flex-col fixed h-full">
        <div className="p-8 flex items-center gap-3">
          <div className="bg-red-600 p-2 rounded-2xl shadow-lg shadow-red-100 text-white">
            <Beef size={32} />
          </div>
          <div>
            <h1 className="text-xl font-black text-gray-800 leading-none">AÇOUGUE</h1>
            <span className="text-xs font-bold text-red-500 tracking-widest">INTELIGENTE SJP</span>
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
            disabled={loadingIA}
            className="w-full bg-gradient-to-br from-amber-400 to-orange-500 text-white p-4 rounded-3xl font-black flex items-center justify-center gap-2 shadow-lg shadow-orange-100 hover:scale-105 transition-transform disabled:opacity-50 disabled:scale-100"
          >
            <BrainCircuit size={20} />
            {loadingIA ? 'PENSANDO...' : 'IA INSIGHTS'}
          </button>
        </div>
      </aside>

      {/* CONTEÚDO PRINCIPAL */}
      <main className="flex-1 ml-72 p-12">
        <div className="max-w-5xl mx-auto">
          
          {/* ÁREA DE INSIGHTS DA IA - Onde a mágica aparece */}
          {insights.length > 0 && (
            <div className="mb-8 bg-amber-50 border-2 border-amber-200 p-6 rounded-[32px] flex items-start gap-4 animate-in fade-in slide-in-from-top-4 duration-500">
              <div className="bg-amber-400 p-2 rounded-xl text-white">
                <BrainCircuit size={24} />
              </div>
              <div className="flex-1">
                <h4 className="font-black text-amber-800 uppercase text-xs tracking-wider mb-2">Sugestões de Vendas Estratégicas</h4>
                {insights.map((txt, i) => (
                  <p key={i} className="text-amber-900 font-bold whitespace-pre-wrap leading-relaxed">
                    {txt}
                  </p>
                ))}
              </div>
              <button onClick={() => setInsights([])} className="text-amber-400 hover:text-amber-600 font-black">X</button>
            </div>
          )}

          {activeTab === 'dashboard' && (
            <div className="space-y-10">
              <header className="flex justify-between items-end">
                <div>
                  <h2 className="text-4xl font-black text-gray-800">Status do Balcão</h2>
                  <p className="text-gray-400 font-medium">Análise de estoque em tempo real</p>
                </div>
                <div className="bg-white p-4 rounded-3xl shadow-sm border border-gray-100 flex items-center gap-4">
                  <div className="bg-green-100 p-2 rounded-xl text-green-600"><TrendingUp size={24} /></div>
                  <div>
                    <p className="text-xs font-bold text-gray-400 uppercase">Vendas Hoje</p>
                    <p className="text-xl font-black text-gray-800">R$ 1.250,00</p>
                  </div>
                </div>
              </header>

              {/* GRID DE CARNES */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {estoque.map((item: any) => (
                  <div key={item.id} className="bg-white p-8 rounded-[40px] shadow-sm border border-gray-100 hover:shadow-xl transition-shadow group">
                    <div className="flex justify-between items-start mb-6">
                      <div className="bg-gray-50 p-3 rounded-2xl group-hover:bg-red-50 group-hover:text-red-600 transition-colors">
                        <Beef size={28} />
                      </div>
                      <span className={`px-4 py-1 rounded-full text-[10px] font-black uppercase ${item.quantidade < 10 ? 'bg-red-100 text-red-600' : 'bg-green-100 text-green-600'}`}>
                        {item.quantidade < 10 ? 'Baixo' : 'Normal'}
                      </span>
                    </div>
                    <h3 className="text-xl font-black text-gray-800 uppercase mb-1">{item.nome}</h3>
                    <div className="flex items-baseline gap-1">
                      <span className="text-3xl font-black text-gray-800">{item.quantidade}</span>
                      <span className="text-gray-400 font-bold uppercase text-xs">Kg em estoque</span>
                    </div>
                    <p className="mt-4 text-green-600 font-black">R$ {item.preco_quilo.toFixed(2)}/kg</p>
                  </div>
                ))}
              </div>

              {/* ÚLTIMAS VENDAS */}
              <div className="bg-white rounded-[40px] p-8 shadow-sm border border-gray-100">
                <h3 className="text-2xl font-black text-gray-800 mb-6 flex items-center gap-3">
                  <History className="text-gray-400" /> Histórico Recente
                </h3>
                <div className="space-y-4">
                  {vendas.map((v: any) => (
                    <div key={v.id} className="flex justify-between items-center p-4 hover:bg-gray-50 rounded-2xl transition-colors border-b border-gray-50 last:border-0">
                      <div>
                        <p className="font-black text-gray-800">{v.cliente_nome}</p>
                        <p className="text-xs text-gray-400 font-bold uppercase">{v.itens_comprados}</p>
                      </div>
                      <div className="text-right">
                        <p className="font-black text-red-600">R$ {v.valor_total}</p>
                        <p className="text-[10px] text-gray-300 font-bold tracking-widest uppercase">WhatsApp: {v.cliente_whatsapp}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {activeTab === 'vendas' && <div className="text-center py-20 font-bold text-gray-400 uppercase">Módulo de Vendas em Construção...</div>}
          {activeTab === 'estoque' && <div className="text-center py-20 font-bold text-gray-400 uppercase">Módulo de Abastecimento em Construção...</div>}
          
        </div>
      </main>
    </div>
  );
};

export default App;
