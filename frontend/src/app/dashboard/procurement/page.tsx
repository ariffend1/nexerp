'use client';

import { useState, useEffect } from 'react';
import { ShoppingCart, Plus, Search, FileText, ChevronRight, Filter } from 'lucide-react';
import { cn } from '@/lib/utils';

export default function ProcurementPage() {
    const [orders, setOrders] = useState([
        { id: 1, po_number: 'PO-2512-0001', supplier: 'IndoSteel Corp', total: '$14,500', status: 'approved', date: '2025-12-18' },
        { id: 2, po_number: 'PO-2512-0002', supplier: 'Chemical Global', total: '$2,200', status: 'pending', date: '2025-12-19' },
        { id: 3, po_number: 'PO-2512-0003', supplier: 'Machine Spare Part Ltd', total: '$8,950', status: 'draft', date: '2025-12-20' },
    ]);

    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <div>
                    <h2 className="text-2xl font-bold text-white">Procurement (Purchase Orders)</h2>
                    <p className="text-slate-400 text-sm">Manage your supply chain and supplier orders</p>
                </div>
                <button className="bg-emerald-600 hover:bg-emerald-500 text-white px-4 py-2 rounded-lg flex items-center gap-2 transition-all shadow-lg shadow-emerald-500/20">
                    <Plus className="w-4 h-4" />
                    Create New PO
                </button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="bg-[#1e293b] p-6 rounded-2xl border border-slate-800">
                    <h3 className="text-slate-500 text-xs font-bold uppercase mb-4 tracking-wider">Inventory Low Warning</h3>
                    <div className="flex items-center gap-4">
                        <div className="p-3 bg-red-500/10 text-red-500 rounded-xl">
                            <FileText className="w-6 h-6" />
                        </div>
                        <div>
                            <p className="text-2xl font-bold text-white">14 Items</p>
                            <p className="text-xs text-slate-500">Suggested to reorder</p>
                        </div>
                    </div>
                </div>
                <div className="bg-[#1e293b] p-6 rounded-2xl border border-slate-800">
                    <h3 className="text-slate-500 text-xs font-bold uppercase mb-4 tracking-wider">Total Pending Amount</h3>
                    <div className="flex items-center gap-4">
                        <div className="p-3 bg-blue-500/10 text-blue-500 rounded-xl">
                            <ShoppingCart className="w-6 h-6" />
                        </div>
                        <div>
                            <p className="text-2xl font-bold text-white">$42,800</p>
                            <p className="text-xs text-slate-500">Across 8 active POs</p>
                        </div>
                    </div>
                </div>
                <div className="bg-[#1e293b] p-6 rounded-2xl border border-slate-800">
                    <h3 className="text-slate-500 text-xs font-bold uppercase mb-4 tracking-wider">Lead Time Average</h3>
                    <div className="flex items-center gap-4">
                        <div className="p-3 bg-indigo-500/10 text-indigo-500 rounded-xl">
                            <ChevronRight className="w-6 h-6" />
                        </div>
                        <div>
                            <p className="text-2xl font-bold text-white">4.2 Days</p>
                            <p className="text-xs text-slate-500">From PO to Receipt</p>
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
                            placeholder="Search POs or Suppliers..."
                            className="w-full bg-slate-900 border border-slate-700 rounded-lg py-2 pl-10 pr-4 text-sm text-white focus:ring-1 focus:ring-emerald-500 outline-none transition-all"
                        />
                    </div>
                    <button className="text-slate-400 hover:text-white flex items-center gap-2 text-sm border border-slate-700 px-3 py-1.5 rounded-lg">
                        <Filter className="w-4 h-4" /> Filter
                    </button>
                </div>

                <div className="overflow-x-auto">
                    <table className="w-full text-left border-collapse">
                        <thead>
                            <tr className="bg-slate-900/50 text-slate-500 text-[10px] font-bold uppercase tracking-widest">
                                <th className="px-6 py-4">PO Number</th>
                                <th className="px-6 py-4">Supplier</th>
                                <th className="px-6 py-4 text-right">Amount</th>
                                <th className="px-6 py-4">Status</th>
                                <th className="px-6 py-4">Date</th>
                                <th className="px-6 py-4"></th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-slate-800/50">
                            {orders.map((order) => (
                                <tr key={order.id} className="hover:bg-slate-800/20 transition-colors group">
                                    <td className="px-6 py-4 font-mono text-xs font-bold text-emerald-400">
                                        {order.po_number}
                                    </td>
                                    <td className="px-6 py-4">
                                        <p className="text-sm font-medium text-white">{order.supplier}</p>
                                    </td>
                                    <td className="px-6 py-4 text-right">
                                        <p className="text-sm font-bold text-white">{order.total}</p>
                                    </td>
                                    <td className="px-6 py-4">
                                        <span className={cn(
                                            "px-3 py-1 rounded-full text-[10px] font-bold uppercase border",
                                            order.status === 'approved' ? 'text-emerald-400 bg-emerald-500/10 border-emerald-500/20' :
                                                order.status === 'pending' ? 'text-amber-400 bg-amber-500/10 border-amber-500/20' :
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
