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
  const [estoque, setEstoque] = useState([]);
  const [vendas, setVendas] = useState([]);
  const [insights, setInsights] = useState<string[]>([]);
  const [loadingIA, setLoadingIA] = useState(false);

  // 1. BUSCAR DADOS (ESTOQUE E VENDAS)
  const fetchData = async () => {
    try {
      const res = await fetch('/api/acougueiro'); // Sua rota FastAPI
      const data = await res.json();
      setEstoque(data.estoque || []);
      setVendas(data.vendas || []);
    } catch (err) {
      console.error("Erro ao carregar dados:", err);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  // 2. GERAR INSIGHTS IA
  const gerarInsights = async () => {
    setLoadingIA(true);
    try {
      const res = await fetch('/api/gerar_insights');
      const data = await res.json();
      setInsights(data.avisos || []);
    } catch (err) {
      setInsights(["Erro ao conectar com a IA em Castanhal."]);
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
            className="w-full bg-gradient-to-br from-amber-400 to-orange-500 text-white p-4 rounded-3xl font-black flex items-center justify-center gap-2 shadow-lg shadow-orange-100 hover:scale-105 transition-transform"
          >
            <BrainCircuit size={20} />
            {loadingIA ? 'PENSANDO...' : 'IA INSIGHTS'}
          </button>
        </div>
      </aside>

      {/* CONTEÚDO */}
      <main className="flex-1 ml-72 p-12">
        <div className="max-w-5xl mx-auto">
          
          {/* ÁREA DE INSIGHTS DA IA */}
          {insights.length > 0 && (
            <div className="mb-8 bg-amber-50 border-2 border-amber-200 p-6 rounded-[32px] flex items-start gap-4">
              <div className="bg-amber-400 p-2 rounded-xl text-white">
                <BrainCircuit size={24} />
              </div>
              <div>
                <h4 className="font-black text-amber-800 uppercase text-xs tracking-wider mb-2">Sugestões para SJP/Castanhal</h4>
                {insights.map((txt, i) => <p key={i} className="text-amber-900 font-bold">{txt}</p>)}
              </div>
            </div>
          )}

          {activeTab === 'dashboard' && (
            <div className="space-y-10">
              <header className="flex justify-between items-end">
                <div>
                  <h2 className="text-4xl font-black text-gray-800">Status do Balcão</h2>
                  <p className="text-gray-400 font-medium">Veja como está o seu estoque hoje</p>
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
                    <p className="mt-4 text-green-600 font-black">R$ {item.preco_quilo}/kg</p>
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

          {/* AS OUTRAS TABS SEGUEM O MESMO PADRÃO... */}
          {activeTab === 'vendas' && <div className="text-center py-20 font-bold text-gray-400 uppercase">Módulo de Vendas em Construção...</div>}
          
        </div>
      </main>
    </div>
  );
};

export default App;