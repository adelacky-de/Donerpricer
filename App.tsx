import React, { useState } from 'react';
import SearchBar from './components/SearchBar';
import RecommendationPanel from './components/RecommendationPanel';
import HistoryTable from './components/HistoryTable';
import PriceChart from './components/PriceChart';
import VintageMap from './components/VintageMap';
import { AnalysisResult, HistoryRecord, Recommendation } from './types';
import { analyzeItemMarket, parseReceiptImage } from './services/geminiService';
import { Newspaper } from 'lucide-react';

const App: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const [itemName, setItemName] = useState<string>('');
  
  const [history, setHistory] = useState<HistoryRecord[]>([]);
  const [recommendation, setRecommendation] = useState<Recommendation | null>(null);

  const handleSearch = async (term: string) => {
    setLoading(true);
    setItemName(term);
    try {
      const result: AnalysisResult = await analyzeItemMarket(term);
      setHistory(result.history);
      setRecommendation(result.recommendation);
    } catch (error) {
      console.error("Error fetching analysis:", error);
      alert("Failed to analyze item. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleReceiptUpload = async (file: File) => {
    setLoading(true);
    try {
      // Convert file to base64
      const reader = new FileReader();
      reader.onload = async () => {
        if (typeof reader.result === 'string') {
          // Remove the data URL prefix
          const base64 = reader.result.split(',')[1];
          const items = await parseReceiptImage(base64);
          
          if (items.length > 0) {
              const firstItem = items[0].name;
              alert(`Receipt scanned! Found ${items.length} items. Analyzing: ${firstItem}`);
              await handleSearch(firstItem);
          } else {
              alert("No recognizable items found on receipt.");
          }
        }
      };
      reader.readAsDataURL(file);
    } catch (error) {
      console.error("Receipt parsing error:", error);
      alert("Failed to parse receipt.");
      setLoading(false);
    }
  };

  const today = new Date().toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });

  return (
    <div className="min-h-screen bg-paper text-ink font-body pb-12 selection:bg-amber-200">
      
      {/* Masthead */}
      <header className="border-b-4 border-double border-ink bg-paper pt-8 pb-4 mb-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <div className="border-b border-ink pb-1 mb-2 flex justify-between items-end text-xs font-mono uppercase tracking-widest">
            <span>Vol. 01</span>
            <span>Est. 2024</span>
            <span>€ 0.50</span>
          </div>
          <h1 className="text-6xl md:text-8xl font-serif font-black tracking-tight uppercase mb-2">
            The Donerprice
          </h1>
          <div className="border-t-2 border-b-2 border-ink py-2 flex justify-between items-center text-sm font-bold uppercase tracking-wider">
             <div className="flex items-center gap-2">
               <Newspaper className="w-4 h-4" />
               <span>Grocery Intelligence</span>
             </div>
             <span>{today}</span>
             <span>Berlin Edition</span>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          
          {/* Left Column: Search & Recommendation (5 cols) */}
          <div className="lg:col-span-5 flex flex-col gap-8">
            <section className="border-2 border-ink bg-white p-1 shadow-[4px_4px_0px_0px_rgba(0,0,0,1)]">
                <div className="border border-ink p-4 h-full">
                    <h2 className="font-serif font-bold text-xl uppercase border-b-2 border-ink mb-4 pb-1 inline-block">Search Archives</h2>
                    <SearchBar 
                    onSearch={handleSearch} 
                    onReceiptUpload={handleReceiptUpload} 
                    isAnalyzing={loading} 
                    />
                </div>
            </section>
            
            <section className="flex-1 min-h-[300px] border-2 border-ink bg-white p-1 shadow-[4px_4px_0px_0px_rgba(0,0,0,1)]">
                 <div className="border border-ink p-4 h-full">
                     <RecommendationPanel data={recommendation} loading={loading} />
                 </div>
            </section>
          </div>

          {/* Right Column: Map, Chart, Table (7 cols) */}
          <div className="lg:col-span-7 flex flex-col gap-8">
             
             {/* Map Component (Between Recommendation logic and Market Fluctuations visually) */}
             <VintageMap data={history} loading={loading} />

             <section className="border-2 border-ink bg-white p-1 shadow-[4px_4px_0px_0px_rgba(0,0,0,1)]">
                <div className="border border-ink p-4">
                     <h2 className="font-serif font-bold text-2xl uppercase border-b-2 border-ink mb-6 text-center">Market Fluctuations</h2>
                     <PriceChart data={history} loading={loading} />
                </div>
            </section>

             <section className="border-2 border-ink bg-white p-1 shadow-[4px_4px_0px_0px_rgba(0,0,0,1)]">
                 <div className="border border-ink p-4">
                     <HistoryTable data={history} loading={loading} />
                 </div>
            </section>
          </div>

        </div>

      </main>
      
      <footer className="max-w-7xl mx-auto px-4 mt-12 mb-8 text-center font-mono text-xs text-stone-500">
         Printed on recycled pixels. Copyright © 2025 Donerprice Gazette.
      </footer>

    </div>
  );
};

export default App;