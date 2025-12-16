import React from 'react';
import { HistoryRecord } from '../types';

interface Props {
  data: HistoryRecord[];
  loading: boolean;
}

const HistoryTable: React.FC<Props> = ({ data, loading }) => {
  return (
    <div className="flex flex-col h-full max-h-[400px]">
      <div className="pb-2 border-b-2 border-ink flex justify-between items-baseline mb-2">
        <h3 className="font-serif font-bold text-lg uppercase">Recent Transactions</h3>
        <span className="font-mono text-xs text-stone-500">Nº Rec: {data.length}</span>
      </div>
      
      <div className="overflow-auto flex-1 border border-ink">
        <table className="w-full text-left text-sm font-mono">
          <thead className="bg-stone-100 border-b border-ink sticky top-0 z-10">
            <tr>
              <th className="px-4 py-2 border-r border-ink text-ink font-bold uppercase text-xs">Date</th>
              <th className="px-4 py-2 border-r border-ink text-ink font-bold uppercase text-xs">Price</th>
              <th className="px-4 py-2 border-r border-ink text-ink font-bold uppercase text-xs">Store</th>
              <th className="px-4 py-2 text-ink font-bold uppercase text-xs">Loc.</th>
            </tr>
          </thead>
          <tbody>
            {loading ? (
               Array.from({ length: 5 }).map((_, i) => (
                <tr key={i} className="animate-pulse bg-white">
                  <td className="px-4 py-3 border-r border-stone-200 border-b border-stone-200"><div className="h-3 w-20 bg-stone-200"></div></td>
                  <td className="px-4 py-3 border-r border-stone-200 border-b border-stone-200"><div className="h-3 w-12 bg-stone-200"></div></td>
                  <td className="px-4 py-3 border-r border-stone-200 border-b border-stone-200"><div className="h-3 w-24 bg-stone-200"></div></td>
                  <td className="px-4 py-3 border-b border-stone-200"><div className="h-3 w-32 bg-stone-200"></div></td>
                </tr>
               ))
            ) : data.length === 0 ? (
                <tr>
                    <td colSpan={4} className="px-6 py-8 text-center text-stone-400 italic font-serif">
                        No records found in the archive.
                    </td>
                </tr>
            ) : (
                data.map((record, idx) => (
                <tr key={idx} className="hover:bg-amber-50 transition-colors border-b border-stone-300 last:border-0">
                    <td className="px-4 py-2 border-r border-stone-300">{record.date}</td>
                    <td className="px-4 py-2 border-r border-stone-300 font-bold">€{record.price.toFixed(2)}</td>
                    <td className="px-4 py-2 border-r border-stone-300 truncate max-w-[100px]" title={record.supermarket}>
                        {record.supermarket}
                    </td>
                    <td className="px-4 py-2 truncate max-w-[120px]" title={record.location}>
                        {record.location}
                    </td>
                </tr>
                ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default HistoryTable;