export interface HistoryRecord {
  date: string;
  price: number;
  supermarket: string;
  location: string;
  lat: number;
  lng: number;
}

export interface Recommendation {
  item: string;
  shouldBuyNow: boolean;
  bestDay: string;
  predictedPrice: number;
  currentAvgPrice: number;
  lazyTax: number;
  confidence: number; // 0-100
  funnyComment: string;
}

export interface AnalysisResult {
  history: HistoryRecord[];
  recommendation: Recommendation;
}

export interface ReceiptItem {
  name: string;
  price: number;
}