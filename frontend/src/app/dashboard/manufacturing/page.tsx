'use client';

import { useState, useEffect } from 'react';
import api from '@/lib/api';
import { Factory, Plus, Search, Calendar, CheckCircle2, Clock, AlertCircle } from 'lucide-react';
import { cn } from '@/lib/utils';

export default function ManufacturingPage() {
    const [jobOrders, setJobOrders] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchJO = async () => {
            try {
                const response = await api.get('/job-orders');
                setJobOrders(response.data);
            } catch (error) {
                console.error('Error fetching job orders:', error);
            } finally {
                setLoading(false);
            }
        };
        fetchJO();
    }, []);

    const getStatusIcon = (status: string) => {
        switch (status) {
            case 'completed': return CheckCircle2;
            case 'in_progress': return Clock;
            case 'scheduled': return Calendar;
            default: return AlertCircle;
        }
    };

    const getStatusColor = (status: string) => {
        switch (status) {
            case 'completed': return 'text-emerald-400 bg-emerald-500/10 border-emerald-500/20';
            case 'in_progress': return 'text-blue-400 bg-blue-500/10 border-blue-500/20';
            case 'scheduled': return 'text-indigo-400 bg-indigo-500/10 border-indigo-500/20';
            default: return 'text-slate-400 bg-slate-500/10 border-slate-500/20';
        }
    };

    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <div>
                    <h2 className="text-2xl font-bold text-white">Manufacturing Orders (SPK)</h2>
                    <p className="text-slate-400 text-sm">Control your production floor and scheduling</p>
                </div>
                <button className="bg-blue-600 hover:bg-blue-500 text-white px-4 py-2 rounded-lg flex items-center gap-2 transition-all shadow-lg shadow-blue-500/20">
                    <Plus className="w-4 h-4" />
                    Create SPK
                </button>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-4 gap-6 mb-8">
                <div className="bg-[#1e293b] p-4 rounded-xl border border-slate-800">
                    <p className="text-slate-500 text-xs font-bold uppercase mb-1">On Schedule</p>
                    <p className="text-xl font-bold text-white">24</p>
                </div>
                <div className="bg-[#1e293b] p-4 rounded-xl border border-slate-800">
                    <p className="text-slate-500 text-xs font-bold uppercase mb-1">In Production</p>
                    <p className="text-xl font-bold text-white">8</p>
                </div>
                <div className="bg-[#1e293b] p-4 rounded-xl border border-slate-800">
                    <p className="text-slate-500 text-xs font-bold uppercase mb-1">Delayed</p>
                    <p className="text-xl font-bold text-red-400">2</p>
                </div>
                <div className="bg-[#1e293b] p-4 rounded-xl border border-slate-800">
                    <p className="text-slate-500 text-xs font-bold uppercase mb-1">Efficiency</p>
                    <p className="text-xl font-bold text-emerald-400">94%</p>
                </div>
            </div>

            <div className="bg-[#1e293b] border border-slate-800 rounded-2xl overflow-hidden shadow-2xl">
                <div className="p-4 border-b border-slate-800 flex items-center justify-between bg-slate-900/20">
                    <div className="relative w-96">
                        <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" />
                        <input
                            type="text"
                            placeholder="Search SPK numbers or products..."
                            className="w-full bg-slate-900 border border-slate-700 rounded-lg py-2 pl-10 pr-4 text-sm text-white focus:ring-1 focus:ring-blue-500 outline-none transition-all"
                        />
                    </div>
                </div>

                <div className="overflow-x-auto">
                    <table className="w-full text-left order-collapse">
                        <thead>
                            <tr className="bg-slate-900/50 text-slate-500 text-[10px] font-bold uppercase tracking-widest">
                                <th className="px-6 py-4">Job Number</th>
                                <th className="px-6 py-4">Product / Item</th>
                                <th className="px-6 py-4">Status</th>
                                <th className="px-6 py-4">Timeline</th>
                                <th className="px-6 py-4 text-right">Approval</th>
                                <th className="px-6 py-4"></th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-slate-800/50">
                            {loading ? (
                                [1, 2, 3].map(i => <tr key={i} className="animate-pulse h-16 bg-slate-800/10"></tr>)
                            ) : jobOrders.length === 0 ? (
                                <tr>
                                    <td colSpan={6} className="px-6 py-20 text-center text-slate-500">
                                        <Factory className="w-12 h-12 mx-auto mb-4 opacity-10" />
                                        <p>No active production orders. Create an SPK to start tracking.</p>
                                    </td>
                                </tr>
                            ) : jobOrders.map((jo: any) => {
                                const StatusIcon = getStatusIcon(jo.status);
                                return (
                                    <tr key={jo.id} className="hover:bg-slate-800/20 transition-colors">
                                        <td className="px-6 py-4 font-mono text-xs font-bold text-blue-400">
                                            {jo.jo_number}
                                        </td>
                                        <td className="px-6 py-4">
                                            <p className="text-sm font-medium text-white">Aluminum Frame 40x40</p>
                                            <p className="text-[10px] text-slate-500">SKU: RM-AL-001</p>
                                        </td>
                                        <td className="px-6 py-4">
                                            <span className={cn(
                                                "inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-[10px] font-bold uppercase border",
                                                getStatusColor(jo.status)
                                            )}>
                                                <StatusIcon className="w-3 h-3" />
                                                {jo.status}
                                            </span>
                                        </td>
                                        <td className="px-6 py-4">
                                            <p className="text-xs text-slate-300">Starts: Dec 20</p>
                                            <p className="text-[10px] text-slate-500">Ends: Dec 25</p>
                                        </td>
                                        <td className="px-6 py-4 text-right">
                                            <span className="text-[10px] font-bold text-amber-500 bg-amber-500/10 px-2 py-0.5 rounded border border-amber-500/20 uppercase">
                                                {jo.approval_status}
                                            </span>
                                        </td>
                                        <td className="px-6 py-4 text-right text-slate-500">
                                            <button className="hover:text-white transition-colors">Details</button>
                                        </td>
                                    </tr>
                                );
                            })}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
}
