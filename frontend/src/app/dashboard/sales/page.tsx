'use client';

import { useState } from 'react';
import { ShoppingBag, Plus, Search, TrendingUp, Users, DollarSign } from 'lucide-react';
import { cn } from '@/lib/utils';

export default function SalesPage() {
    const [sales, setSales] = useState([
        { id: 1, so_number: 'SO-2512-0442', customer: 'Global Motors Ltd', total: '$85,000', status: 'shipped', date: '2025-12-20' },
        { id: 2, so_number: 'SO-2512-0443', customer: 'Nexus Energy', total: '$12,400', status: 'approved', date: '2025-12-20' },
    ]);

    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <div>
                    <h2 className="text-2xl font-bold text-white">Sales & Distribution</h2>
                    <p className="text-slate-400 text-sm">Manage customer orders, shipments, and billing</p>
                </div>
                <button className="bg-indigo-600 hover:bg-indigo-500 text-white px-4 py-2 rounded-lg flex items-center gap-2 transition-all shadow-lg shadow-indigo-500/20">
                    <Plus className="w-4 h-4" />
                    New Sales Order
                </button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="bg-[#1e293b] p-6 rounded-2xl border border-slate-800">
                    <h3 className="text-slate-500 text-xs font-bold uppercase mb-4 tracking-wider">Today's Revenue</h3>
                    <div className="flex items-center gap-4">
                        <div className="p-3 bg-indigo-500/10 text-indigo-500 rounded-xl">
                            <DollarSign className="w-6 h-6" />
                        </div>
                        <div>
                            <p className="text-2xl font-bold text-white">$97,400</p>
                            <p className="text-xs text-emerald-400 flex items-center gap-1">
                                <TrendingUp className="w-3 h-3" /> +14% from yesterday
                            </p>
                        </div>
                    </div>
                </div>
                <div className="bg-[#1e293b] p-6 rounded-2xl border border-slate-800">
                    <h3 className="text-slate-500 text-xs font-bold uppercase mb-4 tracking-wider">Active Customers</h3>
                    <div className="flex items-center gap-4">
                        <div className="p-3 bg-blue-500/10 text-blue-500 rounded-xl">
                            <Users className="w-6 h-6" />
                        </div>
                        <div>
                            <p className="text-2xl font-bold text-white">1,240</p>
                            <p className="text-xs text-slate-500">Across 4 countries</p>
                        </div>
                    </div>
                </div>
                <div className="bg-[#1e293b] p-6 rounded-2xl border border-slate-800">
                    <h3 className="text-slate-500 text-xs font-bold uppercase mb-4 tracking-wider">Pending Shipments</h3>
                    <div className="flex items-center gap-4">
                        <div className="p-3 bg-amber-500/10 text-amber-500 rounded-xl">
                            <ShoppingBag className="w-6 h-6" />
                        </div>
                        <div>
                            <p className="text-2xl font-bold text-white">18</p>
                            <p className="text-xs text-slate-500">Ready for DO</p>
                        </div>
                    </div>
                </div>
            </div>

            <div className="bg-[#1e293b] border border-slate-800 rounded-2xl overflow-hidden shadow-2xl">
                <div className="p-4 border-b border-slate-800 flex items-center justify-between bg-slate-900/20">
                    <div className="relative w-96">
                        <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" />
                        <input
                            type="text"
                            placeholder="Search Orders or Customers..."
                            className="w-full bg-slate-900 border border-slate-700 rounded-lg py-2 pl-10 pr-4 text-sm text-white focus:ring-1 focus:ring-indigo-500 outline-none transition-all"
                        />
                    </div>
                </div>

                <div className="overflow-x-auto">
                    <table className="w-full text-left border-collapse">
                        <thead>
                            <tr className="bg-slate-900/50 text-slate-500 text-[10px] font-bold uppercase tracking-widest">
                                <th className="px-6 py-4">SO Number</th>
                                <th className="px-6 py-4">Customer</th>
                                <th className="px-6 py-4 text-right">Total Amount</th>
                                <th className="px-6 py-4">Status</th>
                                <th className="px-6 py-4">Date</th>
                                <th className="px-6 py-4"></th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-slate-800/50">
                            {sales.map((order) => (
                                <tr key={order.id} className="hover:bg-slate-800/20 transition-colors group">
                                    <td className="px-6 py-4 font-mono text-xs font-bold text-indigo-400">
                                        {order.so_number}
                                    </td>
                                    <td className="px-6 py-4">
                                        <p className="text-sm font-medium text-white">{order.customer}</p>
                                    </td>
                                    <td className="px-6 py-4 text-right">
                                        <p className="text-sm font-bold text-white">{order.total}</p>
                                    </td>
                                    <td className="px-6 py-4">
                                        <span className={cn(
                                            "px-3 py-1 rounded-full text-[10px] font-bold uppercase border",
                                            order.status === 'shipped' ? 'text-blue-400 bg-blue-500/10 border-blue-500/20' :
                                                order.status === 'approved' ? 'text-emerald-400 bg-emerald-500/10 border-emerald-500/20' :
                                                    'text-slate-400 bg-slate-500/10 border-slate-500/20'
                                        )}>
                                            {order.status}
                                        </span>
                                    </td>
                                    <td className="px-6 py-4 text-xs text-slate-500">
                                        {order.date}
                                    </td>
                                    <td className="px-6 py-4 text-right text-slate-500">
                                        <button className="hover:text-white transition-colors">Details</button>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
}
