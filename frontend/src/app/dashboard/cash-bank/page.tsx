'use client';

import { useState } from 'react';
import { Wallet, TrendingUp, TrendingDown, Building2 } from 'lucide-react';

export default function CashBankPage() {
    const [transactions] = useState([
        { id: 1, ref: 'KAS-2025-0001', type: 'receipt', amount: '$5,200', desc: 'Customer Payment - INV-442', date: '2025-12-20' },
        { id: 2, ref: 'KAS-2025-0002', type: 'payment', amount: '$1,400', desc: 'Office Supplies Purchase', date: '2025-12-20' },
    ]);

    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <div>
                    <h2 className="text-2xl font-bold text-white">Cash & Bank Management</h2>
                    <p className="text-slate-400 text-sm">Monitor liquidity and cash flow</p>
                </div>
                <div className="flex gap-3">
                    <button className="bg-emerald-600 hover:bg-emerald-500 text-white px-4 py-2 rounded-lg flex items-center gap-2 transition-all">
                        <TrendingUp className="w-4 h-4" />
                        Receipt
                    </button>
                    <button className="bg-red-600 hover:bg-red-500 text-white px-4 py-2 rounded-lg flex items-center gap-2 transition-all">
                        <TrendingDown className="w-4 h-4" />
                        Payment
                    </button>
                </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                <div className="bg-[#1e293b] p-6 rounded-2xl border border-slate-800">
                    <h3 className="text-slate-500 text-xs font-bold uppercase mb-4 tracking-wider">Cash on Hand</h3>
                    <div className="flex items-center gap-4">
                        <div className="p-3 bg-emerald-500/10 text-emerald-500 rounded-xl">
                            <Wallet className="w-6 h-6" />
                        </div>
                        <div>
                            <p className="text-2xl font-bold text-white">$42,800</p>
                            <p className="text-xs text-emerald-400">+12% this month</p>
                        </div>
                    </div>
                </div>
                <div className="bg-[#1e293b] p-6 rounded-2xl border border-slate-800">
                    <h3 className="text-slate-500 text-xs font-bold uppercase mb-4 tracking-wider">Bank Balance</h3>
                    <div className="flex items-center gap-4">
                        <div className="p-3 bg-blue-500/10 text-blue-500 rounded-xl">
                            <Building2 className="w-6 h-6" />
                        </div>
                        <div>
                            <p className="text-2xl font-bold text-white">$328,550</p>
                            <p className="text-xs text-slate-500">Across 3 accounts</p>
                        </div>
                    </div>
                </div>
                <div className="bg-[#1e293b] p-6 rounded-2xl border border-slate-800">
                    <h3 className="text-slate-500 text-xs font-bold uppercase mb-4 tracking-wider">Today&apos;s Receipts</h3>
                    <div className="flex items-center gap-4">
                        <div className="p-3 bg-cyan-500/10 text-cyan-500 rounded-xl">
                            <TrendingUp className="w-6 h-6" />
                        </div>
                        <div>
                            <p className="text-2xl font-bold text-white">$24,100</p>
                            <p className="text-xs text-slate-500">12 transactions</p>
                        </div>
                    </div>
                </div>
                <div className="bg-[#1e293b] p-6 rounded-2xl border border-slate-800">
                    <h3 className="text-slate-500 text-xs font-bold uppercase mb-4 tracking-wider">Today&apos;s Payments</h3>
                    <div className="flex items-center gap-4">
                        <div className="p-3 bg-orange-500/10 text-orange-500 rounded-xl">
                            <TrendingDown className="w-6 h-6" />
                        </div>
                        <div>
                            <p className="text-2xl font-bold text-white">$8,760</p>
                            <p className="text-xs text-slate-500">5 transactions</p>
                        </div>
                    </div>
                </div>
            </div>

            <div className="bg-[#1e293b] border border-slate-800 rounded-2xl overflow-hidden shadow-2xl">
                <div className="p-4 border-b border-slate-800 bg-slate-900/20">
                    <h3 className="text-white font-semibold">Recent Transactions</h3>
                </div>

                <div className="overflow-x-auto">
                    <table className="w-full text-left border-collapse">
                        <thead>
                            <tr className="bg-slate-900/50 text-slate-500 text-[10px] font-bold uppercase tracking-widest">
                                <th className="px-6 py-4">Ref Number</th>
                                <th className="px-6 py-4">Type</th>
                                <th className="px-6 py-4">Description</th>
                                <th className="px-6 py-4 text-right">Amount</th>
                                <th className="px-6 py-4">Date</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-slate-800/50">
                            {transactions.map((tx) => (
                                <tr key={tx.id} className="hover:bg-slate-800/20 transition-colors">
                                    <td className="px-6 py-4 font-mono text-xs font-bold text-cyan-400">{tx.ref}</td>
                                    <td className="px-6 py-4">
                                        <span className={`px-2 py-1 rounded text-[10px] font-bold uppercase ${tx.type === 'receipt' ? 'text-emerald-400 bg-emerald-500/10' : 'text-red-400 bg-red-500/10'
                                            }`}>
                                            {tx.type}
                                        </span>
                                    </td>
                                    <td className="px-6 py-4 text-sm text-white">{tx.desc}</td>
                                    <td className={`px-6 py-4 text-right text-sm font-bold ${tx.type === 'receipt' ? 'text-emerald-400' : 'text-red-400'
                                        }`}>{tx.amount}</td>
                                    <td className="px-6 py-4 text-xs text-slate-500">{tx.date}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
}
