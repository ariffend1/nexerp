'use client';

import { useState, useEffect } from 'react';
import { Plus, Search, Building2 } from 'lucide-react';
import { cn } from '@/lib/utils';

export default function PartnersPage() {
    const [partners, setPartners] = useState([]);
    const [loading, setLoading] = useState(true);
    const [activeTab, setActiveTab] = useState<'customers' | 'suppliers'>('customers');

    useEffect(() => {
        const fetchPartners = async () => {
            try {
                // Placeholder - can be connected to actual API later
                setPartners([]);
            } catch (error) {
                console.error('Error fetching partners:', error);
            } finally {
                setLoading(false);
            }
        };
        fetchPartners();
    }, [activeTab]);

    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <div>
                    <h2 className="text-2xl font-bold text-white">Partners</h2>
                    <p className="text-slate-400 text-sm">Manage customers, suppliers, and business partners</p>
                </div>
                <button
                    onClick={() => alert('Add Partner - Coming Soon')}
                    className="bg-blue-600 hover:bg-blue-500 text-white px-4 py-2 rounded-lg flex items-center gap-2 transition-all shadow-lg shadow-blue-500/20"
                >
                    <Plus className="w-4 h-4" />
                    Add Partner
                </button>
            </div>

            {/* Tabs */}
            <div className="flex gap-2">
                <button
                    onClick={() => setActiveTab('customers')}
                    className={cn(
                        "px-4 py-2 rounded-lg font-medium transition-all",
                        activeTab === 'customers'
                            ? "bg-blue-600 text-white"
                            : "bg-slate-800 text-slate-400 hover:text-white"
                    )}
                >
                    Customers
                </button>
                <button
                    onClick={() => setActiveTab('suppliers')}
                    className={cn(
                        "px-4 py-2 rounded-lg font-medium transition-all",
                        activeTab === 'suppliers'
                            ? "bg-blue-600 text-white"
                            : "bg-slate-800 text-slate-400 hover:text-white"
                    )}
                >
                    Suppliers
                </button>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-4 gap-6 mb-8">
                <div className="bg-[#1e293b] p-4 rounded-xl border border-slate-800">
                    <p className="text-slate-500 text-xs font-bold uppercase mb-1">Total {activeTab}</p>
                    <p className="text-xl font-bold text-white">0</p>
                </div>
                <div className="bg-[#1e293b] p-4 rounded-xl border border-slate-800">
                    <p className="text-slate-500 text-xs font-bold uppercase mb-1">Active</p>
                    <p className="text-xl font-bold text-emerald-400">0</p>
                </div>
                <div className="bg-[#1e293b] p-4 rounded-xl border border-slate-800">
                    <p className="text-slate-500 text-xs font-bold uppercase mb-1">Total Transactions</p>
                    <p className="text-xl font-bold text-white">0</p>
                </div>
                <div className="bg-[#1e293b] p-4 rounded-xl border border-slate-800">
                    <p className="text-slate-500 text-xs font-bold uppercase mb-1">Outstanding</p>
                    <p className="text-xl font-bold text-amber-400">Rp 0</p>
                </div>
            </div>

            <div className="bg-[#1e293b] border border-slate-800 rounded-2xl overflow-hidden shadow-2xl">
                <div className="p-4 border-b border-slate-800 flex items-center justify-between bg-slate-900/20">
                    <div className="relative w-96">
                        <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" />
                        <input
                            type="text"
                            placeholder={`Search ${activeTab}...`}
                            className="w-full bg-slate-900 border border-slate-700 rounded-lg py-2 pl-10 pr-4 text-sm text-white focus:ring-1 focus:ring-blue-500 outline-none transition-all"
                        />
                    </div>
                </div>

                <div className="overflow-x-auto">
                    <table className="w-full text-left">
                        <thead>
                            <tr className="bg-slate-900/50 text-slate-500 text-[10px] font-bold uppercase tracking-widest">
                                <th className="px-6 py-4">Code</th>
                                <th className="px-6 py-4">Name</th>
                                <th className="px-6 py-4">Contact</th>
                                <th className="px-6 py-4">Phone</th>
                                <th className="px-6 py-4">Email</th>
                                <th className="px-6 py-4"></th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-slate-800/50">
                            {loading ? (
                                [1, 2, 3].map(i => <tr key={i} className="animate-pulse h-16 bg-slate-800/10"></tr>)
                            ) : partners.length === 0 ? (
                                <tr>
                                    <td colSpan={6} className="px-6 py-20 text-center text-slate-500">
                                        <Building2 className="w-12 h-12 mx-auto mb-4 opacity-10" />
                                        <p>No {activeTab} found. Add your first {activeTab === 'customers' ? 'customer' : 'supplier'} to get started.</p>
                                    </td>
                                </tr>
                            ) : null}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
}
