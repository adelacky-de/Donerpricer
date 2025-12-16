import React, { useState, useRef } from 'react';
import { Search, Loader2, Camera } from 'lucide-react';

interface SearchBarProps {
  onSearch: (term: string) => void;
  onReceiptUpload: (file: File) => void;
  isAnalyzing: boolean;
}

const SearchBar: React.FC<SearchBarProps> = ({ onSearch, onReceiptUpload, isAnalyzing }) => {
  const [term, setTerm] = useState('');
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (term.trim()) onSearch(term);
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      onReceiptUpload(e.target.files[0]);
    }
  };

  return (
    <div className="flex flex-col gap-4">
        
        {/* Search Input */}
        <form onSubmit={handleSubmit} className="flex gap-2">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-ink w-5 h-5" />
            <input
              type="text"
              className="w-full pl-10 pr-4 py-3 bg-paper border-2 border-ink rounded-none focus:outline-none focus:ring-1 focus:ring-ink transition-all font-mono placeholder:text-stone-400 text-sm"
              placeholder="Query Item Name..."
              value={term}
              onChange={(e) => setTerm(e.target.value)}
            />
          </div>
          <button
            type="submit"
            disabled={isAnalyzing}
            className="px-6 py-3 bg-ink hover:bg-stone-800 text-white font-serif font-bold tracking-widest uppercase transition-colors flex items-center gap-2 disabled:opacity-50 border-2 border-ink"
          >
            {isAnalyzing ? <Loader2 className="animate-spin w-4 h-4" /> : 'GO'}
          </button>
        </form>

        {/* Upload Action */}
        <div className="flex items-center justify-between pt-3 border-t border-stone-300 border-dashed mt-1">
          <span className="text-sm italic font-serif text-stone-600">Have a receipt?</span>
          <button 
            onClick={() => fileInputRef.current?.click()}
            className="flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-ink hover:underline decoration-2 underline-offset-4"
          >
            <Camera className="w-4 h-4" />
            Submit Evidence
          </button>
          <input 
            type="file" 
            ref={fileInputRef} 
            className="hidden" 
            accept="image/*"
            onChange={handleFileChange}
          />
        </div>
    </div>
  );
};

export default SearchBar;