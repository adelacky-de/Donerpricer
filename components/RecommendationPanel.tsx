import React from 'react';
import { Recommendation } from '../types';
import { TrendingDown, TrendingUp, AlertTriangle, CheckCircle2, ShoppingBag } from 'lucide-react';

interface Props {
  data: Recommendation | null;
  loading: boolean;
}

const RecommendationPanel: React.FC<Props> = ({ data, loading }) => {
  if (loading) {
    return (
      <div className="h-full flex flex-col items-center justify-center text-stone-400 animate-pulse py-10">
        <div className="w-16 h-16 border-4 border-stone-200 rounded-full mb-4"></div>
        <div className="h-4 w-32 bg-stone-200 mb-2"></div>
        <div className="h-2 w-48 bg-stone-200"></div>
        <p className="mt-4 font-mono text-xs uppercase tracking-widest">Consulting the experts...</p>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="h-full flex flex-col items-center justify-center text-stone-400 text-center py-10">
        <div className="border-2 border-stone-200 p-4 rounded-full mb-4">
            <ShoppingBag className="w-8 h-8 opacity-40" />
        </div>
        <p className="font-serif italic text-lg text-stone-500">Awaiting your query.</p>
        <p className="font-mono text-xs mt-2 text-stone-400 uppercase">Search an item to read the report.</p>
      </div>
    );
  }

  const isGoodBuy = data.shouldBuyNow;

  return (
    <div className="flex flex-col h-full">
      <div className="border-b-4 border-double border-ink pb-4 mb-4 text-center">
          <span className="bg-ink text-white px-2 py-1 text-xs font-bold uppercase tracking-widest mb-2 inline-block">
              Official Verdict
          </span>
          <h2 className="text-4xl font-serif font-black uppercase tracking-tight leading-none mt-2">
            {isGoodBuy ? "BUY IT NOW!" : "HOLD YOUR WALLET!"}
          </h2>
      </div>

      <div className="flex-1 flex flex-col justify-between gap-6">
        <div className="grid grid-cols-2 gap-4 border-b border-stone-300 pb-4">
            <div className="border-r border-stone-300 pr-4">
                <span className="font-mono text-xs uppercase text-stone-500 block mb-1">Forecasted Price</span>
                <span className="font-serif text-3xl font-bold">€{data.predictedPrice.toFixed(2)}</span>
            </div>
             <div className="text-right pl-4">
                <span className="font-mono text-xs uppercase text-stone-500 block mb-1">Target Day</span>
                <span className="font-serif text-xl font-bold italic border-b-2 border-transparent inline-block decoration-orange-500">
                    {data.bestDay}
                </span>
            </div>
        </div>

        <div className="font-serif text-lg leading-relaxed">
            <span className="float-left text-4xl font-black mr-2 leading-none mt-[-4px]">"</span>
            {data.funnyComment}
            <span className="align-top text-xl leading-none">"</span>
        </div>

        <div className="bg-stone-100 p-4 border border-stone-300 relative">
             <div className="absolute -top-2 left-4 bg-white px-1 font-mono text-xs font-bold uppercase tracking-widest border border-stone-300 text-stone-500">
                 Market Analysis
             </div>
            {!isGoodBuy ? (
             <div className="flex items-start gap-3 mt-1">
                 <TrendingUp className="w-5 h-5 text-ink mt-1 shrink-0" />
                 <div>
                     <p className="font-bold text-sm uppercase">Impatience Tax</p>
                     <p className="text-sm font-serif">
                         Buying today incurs a penalty of <span className="font-bold underline decoration-wavy decoration-red-900">€{data.lazyTax.toFixed(2)}</span> compared to waiting.
                     </p>
                 </div>
             </div>
            ) : (
             <div className="flex items-start gap-3 mt-1">
                 <TrendingDown className="w-5 h-5 text-ink mt-1 shrink-0" />
                 <div>
                     <p className="font-bold text-sm uppercase">Discount Opportunity</p>
                     <p className="text-sm font-serif">
                         Current market value is <span className="font-bold underline decoration-wavy decoration-green-900">€{Math.abs(data.lazyTax).toFixed(2)}</span> below the moving average.
                     </p>
                 </div>
             </div>
            )}
        </div>
        
        <div className="text-right font-mono text-xs text-stone-400 uppercase tracking-widest">
            Confidence Index: {data.confidence}/100
        </div>
      </div>
    </div>
  );
};

export default RecommendationPanel;