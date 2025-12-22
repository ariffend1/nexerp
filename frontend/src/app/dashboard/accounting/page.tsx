'use client';

import { useState } from 'react';
import { Calculator, Wallet, Receipt, ArrowRightLeft, Search, Plus } from 'lucide-react';

export default function AccountingPage() {
    const [journals, setJournals] = useState([
        { id: 1, ref: 'JV-2512-001', desc: 'Inventory Receipt - PO-001', amount: '$14,500', status: 'posted', date: '2025-12-20' },
        { id: 2, ref: 'JV-2512-002', desc: 'Sales Recording - SO-442', amount: '$85,000', status: 'pending', date: '2025-12-20' },
    ]);

    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <div>
                    <h2 className="text-2xl font-bold text-white">Accounting & Finance</h2>
                    <p className="text-slate-400 text-sm">General Ledger, Journals, and Financial Statements</p>
                </div>
                <div className="flex gap-3">
                    <button className="bg-slate-800 hover:bg-slate-700 text-white px-4 py-2 rounded-lg flex items-center gap-2 border border-slate-700 transition-all">
                        Chart of Accounts
                    </button>
                    <button className="bg-blue-600 hover:bg-blue-500 text-white px-4 py-2 rounded-lg flex items-center gap-2 shadow-lg shadow-blue-500/20">
                        <Plus className="w-4 h-4" />
                        New Journal
                    </button>
                </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                <div className="bg-[#1e293b] p-5 rounded-2xl border border-slate-800">
                    <p className="text-slate-500 text-xs font-bold uppercase mb-2">Total Assets</p>
                    <p className="text-xl font-bold text-white">$1,240,000</p>
                </div>
                <div className="bg-[#1e293b] p-5 rounded-2xl border border-slate-800">
                    <p className="text-slate-500 text-xs font-bold uppercase mb-2">Total Liabilities</p>
                    <p className="text-xl font-bold text-red-400">$450,000</p>
                </div>
                <div className="bg-[#1e293b] p-5 rounded-2xl border border-slate-800">
                    <p className="text-slate-500 text-xs font-bold uppercase mb-2">Cash on Hand</p>
                    <p className="text-xl font-bold text-emerald-400">$320,500</p>
                </div>
                <div className="bg-[#1e293b] p-5 rounded-2xl border border-slate-800">
                    <p className="text-slate-500 text-xs font-bold uppercase mb-2">P&L (Month)</p>
                    <p className="text-xl font-bold text-blue-400">+$124,000</p>
                </div>
            </div>

            <div className="bg-[#1e293b] border border-slate-800 rounded-2xl overflow-hidden shadow-2xl">
                <div className="p-4 border-b border-slate-800 flex items-center justify-between bg-slate-900/20">
                    <h3 className="text-white font-semibold">General Ledger (Recent Journals)</h3>
                    <div className="relative w-72">
                        <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" />
                        <input
                            type="text"
                            placeholder="Filter journals..."
                            className="w-full bg-slate-900 border border-slate-700 rounded-lg py-1.5 pl-10 pr-4 text-sm text-white focus:ring-1 focus:ring-blue-500 outline-none"
                        />
                    </div>
                </div>

                <div className="overflow-x-auto">
                    <table className="w-full text-left border-collapse">
                        <thead>
                            <tr className="bg-slate-900/50 text-slate-500 text-[10px] font-bold uppercase tracking-widest border-b border-slate-800">
                                <th className="px-6 py-4">Ref Number</th>
                                <th className="px-6 py-4">Description</th>
                                <th className="px-6 py-4 text-right">Total Amount</th>
                                <th className="px-6 py-4">Status</th>
                                <th className="px-6 py-4">Date</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-slate-800/50">
                            {journals.map((j) => (
                                <tr key={j.id} className="hover:bg-slate-800/20 transition-colors">
                                    <td className="px-6 py-4 font-mono text-xs font-bold text-blue-400">{j.ref}</td>
                                    <td className="px-6 py-4 text-sm text-white">{j.desc}</td>
                                    <td className="px-6 py-4 text-right text-sm font-bold text-white">{j.amount}</td>
                                    <td className="px-6 py-4">
                                        <span className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase border ${j.status === 'posted' ? 'text-emerald-400 bg-emerald-500/10 border-emerald-500/20' : 'text-amber-400 bg-amber-500/10 border-amber-500/20'
                                            }`}>
                                            {j.status}
                                        </span>
                                    </td>
                                    <td className="px-6 py-4 text-xs text-slate-500">{j.date}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
}
