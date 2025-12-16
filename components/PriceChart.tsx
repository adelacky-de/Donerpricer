import React from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';
import { HistoryRecord } from '../types';

interface Props {
  data: HistoryRecord[];
  loading: boolean;
}

const PriceChart: React.FC<Props> = ({ data, loading }) => {
    // Sort data by date just in case
    const sortedData = [...data].sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime());

    if (loading) {
        return (
            <div className="h-[300px] flex items-center justify-center">
                 <div className="font-mono text-xs uppercase animate-pulse text-stone-400">Drawing Chart...</div>
            </div>
        )
    }

  return (
    <div className="h-[300px] flex flex-col w-full">
      <div className="flex-1 w-full min-h-0 bg-stone-50 border border-stone-200 p-2">
        {data.length === 0 ? (
            <div className="h-full flex items-center justify-center text-stone-400 text-sm font-serif italic">
                Awaiting data points for visualization.
            </div>
        ) : (
            <ResponsiveContainer width="100%" height="100%">
            <LineChart
                data={sortedData}
                margin={{
                top: 10,
                right: 30,
                left: 0,
                bottom: 5,
                }}
            >
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#d6d3d1" />
                <XAxis 
                    dataKey="date" 
                    tick={{fontSize: 10, fill: '#1a1a1a', fontFamily: 'Courier Prime'}} 
                    tickLine={true}
                    axisLine={true}
                    stroke="#1a1a1a"
                    tickFormatter={(value) => {
                        const date = new Date(value);
                        return `${date.getDate()}/${date.getMonth() + 1}`;
                    }}
                />
                <YAxis 
                    domain={['auto', 'auto']}
                    tick={{fontSize: 10, fill: '#1a1a1a', fontFamily: 'Courier Prime'}} 
                    tickLine={true}
                    axisLine={true}
                    stroke="#1a1a1a"
                    tickFormatter={(value) => `€${value}`}
                />
                <Tooltip 
                    contentStyle={{ 
                        borderRadius: '0px', 
                        border: '2px solid #1a1a1a', 
                        backgroundColor: '#fff',
                        fontFamily: 'Courier Prime',
                        fontSize: '12px'
                    }}
                    itemStyle={{ color: '#1a1a1a', fontWeight: 'bold' }}
                    formatter={(value: number) => [`€${value.toFixed(2)}`, 'Value']}
                />
                <Line 
                    type="stepAfter" 
                    dataKey="price" 
                    stroke="#1a1a1a" 
                    strokeWidth={2}
                    dot={{ stroke: '#1a1a1a', strokeWidth: 2, r: 3, fill: '#fff' }}
                    activeDot={{ r: 5, fill: '#1a1a1a' }}
                />
            </LineChart>
            </ResponsiveContainer>
        )}
      </div>
    </div>
  );
};

export default PriceChart;