import { AnalysisResult, ReceiptItem } from "../types";
import { supabase } from "./supabaseClient";

import { AnalysisResult, ReceiptItem, HistoryRecord, Recommendation } from "../types";
import { supabase } from "./supabaseClient";

// Helper to generate a random date within the last 30 days
const getRandomDate = (daysAgo: number) => {
  const date = new Date();
  date.setDate(date.getDate() - Math.floor(Math.random() * daysAgo));
  return date.toISOString().split('T')[0];
};

// Helper to generate a random Berlin coordinate
const getRandomBerlinCoord = () => {
  const lat = 52.4 + Math.random() * 0.2; // ~52.4 to 52.6
  const lng = 13.3 + Math.random() * 0.2; // ~13.3 to 13.5
  return { lat: parseFloat(lat.toFixed(4)), lng: parseFloat(lng.toFixed(4)) };
};

export const analyzeItemMarket = async (itemName: string): Promise<AnalysisResult> => {
  // Simulate network delay
  await new Promise(resolve => setTimeout(resolve, 1000));

  const supermarkets = ["Aldi", "Lidl", "Rewe", "Edeka", "Netto"];
  const berlinLocations = ["Kreuzberg", "Mitte", "Neukölln", "Prenzlauer Berg", "Friedrichshain", "Charlottenburg"];

  const history: HistoryRecord[] = Array.from({ length: 15 }).map(() => {
    const { lat, lng } = getRandomBerlinCoord();
    return {
      date: getRandomDate(30),
      price: parseFloat((Math.random() * 2 + 1).toFixed(2)), // Price between 1.00 and 3.00
      supermarket: supermarkets[Math.floor(Math.random() * supermarkets.length)],
      location: `Berlin - ${berlinLocations[Math.floor(Math.random() * berlinLocations.length)]}`,
      lat,
      lng,
    };
  }).sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime()); // Sort by date

  const currentAvgPrice = history.reduce((sum, record) => sum + record.price, 0) / history.length;
  const predictedPrice = parseFloat((currentAvgPrice * (1 - Math.random() * 0.1)).toFixed(2)); // 0-10% cheaper
  const lazyTax = parseFloat((currentAvgPrice - predictedPrice).toFixed(2));
  const shouldBuyNow = lazyTax > 0.1; // If saving more than 0.10€, it's a good buy
  const confidence = Math.floor(Math.random() * 40) + 60; // 60-100%

  const recommendation: Recommendation = {
    item: itemName,
    shouldBuyNow,
    bestDay: ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"][Math.floor(Math.random() * 7)],
    predictedPrice,
    currentAvgPrice: parseFloat(currentAvgPrice.toFixed(2)),
    lazyTax,
    confidence,
    funnyComment: shouldBuyNow
      ? `The stars align! This ${itemName} is practically begging to be bought. Don't miss out!`
      : `Hold your horses! Buying ${itemName} today would incur the dreaded 'too lazy to wait' tax of €${lazyTax.toFixed(2)}. Patience, young padawan.`,
  };

  const result: AnalysisResult = { history, recommendation };

  // --- Supabase Integration ---
  // Fire and forget storage. We don't block the UI if this fails.
  if (supabase) {
    (async () => {
        try {
            // Assumes a table 'price_history' exists with these columns.
            const rowsToInsert = result.history.map(h => ({
                item_name: itemName,
                price: h.price,
                date: h.date,
                supermarket: h.supermarket,
                location: h.location,
                lat: h.lat,
                lng: h.lng,
                created_at: new Date().toISOString()
            }));
            
            const { error } = await supabase.from('price_history').insert(rowsToInsert);
            if (error) {
                console.warn("Supabase storage error:", error.message);
            } else {
                console.log(`Stored ${rowsToInsert.length} records in Supabase.`);
            }
        } catch (err) {
            console.warn("Failed to interact with Supabase:", err);
        }
    })();
  }

  return result;
};

export const parseReceiptImage = async (base64Image: string): Promise<ReceiptItem[]> => {
  // Simulate network delay
  await new Promise(resolve => setTimeout(resolve, 500));

  // Mock receipt parsing
  const mockItems: ReceiptItem[] = [
    { name: "Milk", price: 1.19 },
    { name: "Bread", price: 2.49 },
    { name: "Eggs (10)", price: 3.29 },
  ];

  return mockItems;
};