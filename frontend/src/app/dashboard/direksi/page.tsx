'use client';

import { useState, useEffect } from 'react';
import api from '@/lib/api';
import KPICard from '@/components/dashboard/KPICard';
import { TrendingUp, DollarSign, Target, PieChart, Download, BarChart } from 'lucide-react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

export default function DireksiDashboard() {
    const [metrics, setMetrics] = useState<any>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchMetrics();
    }, []);

    const fetchMetrics = async () => {
        try {
            const response = await api.get('/dashboards/direksi');
            setMetrics(response.data.metrics);
        } catch (error) {
            console.error('Error fetching Direksi metrics:', error);
        } finally {
            setLoading(false);
        }
    };

    if (loading) {
        return (
            <div className="flex items-center justify-center min-h-screen">
                <div className="text-center">
                    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-red-500 mx-auto mb-4"></div>
                    <p className="text-slate-400">Loading executive dashboard...</p>
                </div>
            </div>
        );
    }

    return (
        <div className="space-y-6">
            {/* Header */}
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-3xl font-bold text-white mb-2">Direksi Dashboard</h1>
                    <p className="text-slate-400">Executive Summary & Strategic Insights</p>
                </div>
                <div className="flex items-center gap-3">
                    <button className="bg-red-600 hover:bg-red-500 text-white px-4 py-2 rounded-lg transition-all flex items-center gap-2">
                        <Download className="w-4 h-4" />
                        Export PDF
                    </button>
                    <button className="bg-slate-800 hover:bg-slate-700 text-white px-4 py-2 rounded-lg transition-all">
                        Board Materials
                    </button>
                </div>
            </div>

            {/* Top-Level KPIs */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <KPICard
                    title="Revenue (YoY)"
                    value={`Rp ${(metrics?.revenue_current_year / 1000000000).toFixed(2)}B`}
                    icon={DollarSign}
                    color="red"
                    trend={metrics?.yoy_growth_percent}
                    trendLabel={`+${metrics?.yoy_growth_percent}% YoY`}
                />
                <KPICard
                    title="Net Profit Margin"
                    value={`${metrics?.net_profit_margin}%`}
                    icon={TrendingUp}
                    color="green"
                    subtitle="Industry avg: 15%"
                />
                <KPICard
                    title="ROI"
                    value={`${metrics?.roi_percent}%`}
                    icon={Target}
                    color="purple"
                    trend={5.2}
                />
                <KPICard
                    title="Assets"
                    value={`Rp ${(metrics?.total_assets / 1000000000).toFixed(2)}B`}
                    icon={PieChart}
                    color="cyan"
                />
            </div>

            {/* Financial Summary */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                {/* P&L Summary */}
                <div className="lg:col-span-2 bg-[#1e293b] border border-slate-800 rounded-2xl p-6">
                    <h3 className="text-white font-semibold mb-4">Profit & Loss Summary</h3>
                    <div className="space-y-3">
                        <div className="flex justify-between items-center p-4 bg-slate-900/50 rounded-lg border-l-4 border-emerald-500">
                            <span className="text-slate-300 font-medium">Total Revenue</span>
                            <span className="text-2xl font-bold text-emerald-400">
                                Rp {(metrics?.revenue_current_year / 1000000000).toFixed(2)}B
                            </span>
                        </div>
                        <div className="flex justify-between items-center p-4 bg-slate-900/50 rounded-lg border-l-4 border-blue-500">
                            <span className="text-slate-300 font-medium">Gross Profit</span>
                            <span className="text-xl font-bold text-white">
                                Rp {(metrics?.revenue_current_year * 0.35 / 1000000000).toFixed(2)}B
                            </span>
                        </div>
                        <div className="flex justify-between items-center p-4 bg-slate-900/50 rounded-lg border-l-4 border-purple-500">
                            <span className="text-slate-300 font-medium">Operating Profit</span>
                            <span className="text-xl font-bold text-white">
                                Rp {(metrics?.revenue_current_year * 0.22 / 1000000000).toFixed(2)}B
                            </span>
                        </div>
                        <div className="flex justify-between items-center p-4 bg-gradient-to-r from-emerald-900/30 to-emerald-800/20 rounded-lg border-l-4 border-emerald-400">
                            <span className="text-white font-semibold">Net Profit</span>
                            <span className="text-3xl font-bold text-emerald-400">
                                Rp {(metrics?.net_profit / 1000000000).toFixed(2)}B
                            </span>
                        </div>
                    </div>
                </div>

                {/* Financial Ratios */}
                <div className="bg-[#1e293b] border border-slate-800 rounded-2xl p-6">
                    <h3 className="text-white font-semibold mb-4">Key Ratios</h3>
                    <div className="space-y-4">
                        <div>
                            <div className="flex justify-between mb-2">
                                <span className="text-slate-400 text-sm">Debt-to-Equity</span>
                                <span className="text-white font-bold">{metrics?.debt_to_equity_ratio}</span>
                            </div>
                            <div className="h-2 bg-slate-900 rounded-full">
                                <div className="h-full bg-amber-500 rounded-full" style={{ width: `${Math.min(metrics?.debt_to_equity_ratio * 50, 100)}%` }} />
                            </div>
                        </div>
                        <div>
                            <div className="flex justify-between mb-2">
                                <span className="text-slate-400 text-sm">Asset Turnover</span>
                                <span className="text-white font-bold">{metrics?.asset_turnover_ratio}x</span>
                            </div>
                            <div className="h-2 bg-slate-900 rounded-full">
                                <div className="h-full bg-emerald-500 rounded-full" style={{ width: `${metrics?.asset_turnover_ratio * 50}%` }} />
                            </div>
                        </div>
                        <div>
                            <div className="flex justify-between mb-2">
                                <span className="text-slate-400 text-sm">ROE</span>
                                <span className="text-white font-bold">28.3%</span>
                            </div>
                            <div className="h-2 bg-slate-900 rounded-full">
                                <div className="h-full bg-purple-500 rounded-full" style={{ width: '70%' }} />
                            </div>
                        </div>
                        <div>
                            <div className="flex justify-between mb-2">
                                <span className="text-slate-400 text-sm">Quick Ratio</span>
                                <span className="text-white font-bold">1.8</span>
                            </div>
                            <div className="h-2 bg-slate-900 rounded-full">
                                <div className="h-full bg-cyan-500 rounded-full" style={{ width: '90%' }} />
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            {/* Balance Sheet & Strategic Progress */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Balance Sheet */}
                <div className="bg-[#1e293b] border border-slate-800 rounded-2xl p-6">
                    <h3 className="text-white font-semibold mb-4">Balance Sheet Highlights</h3>
                    <div className="space-y-3">
                        <div className="flex justify-between p-3 bg-slate-900/50 rounded-lg">
                            <span className="text-slate-400">Total Assets</span>
                            <span className="text-white font-bold">Rp {(metrics?.total_assets / 1000000000).toFixed(2)}B</span>
                        </div>
                        <div className="flex justify-between p-3 bg-slate-900/50 rounded-lg">
                            <span className="text-slate-400">Total Equity</span>
                            <span className="text-white font-bold">Rp {(metrics?.total_equity / 1000000000).toFixed(2)}B</span>
                        </div>
                        <div className="flex justify-between p-3 bg-slate-900/50 rounded-lg">
                            <span className="text-slate-400">Cash & Equivalents</span>
                            <span className="text-white font-bold">Rp {(metrics?.total_assets * 0.15 / 1000000000).toFixed(2)}B</span>
                        </div>
                        <div className="flex justify-between p-3 bg-slate-900/50 rounded-lg">
                            <span className="text-slate-400">Book Value per Share</span>
                            <span className="text-white font-bold">Rp 12,450</span>
                        </div>
                    </div>
                </div>

                {/* Strategic Initiatives Progress */}
                <div className="bg-[#1e293b] border border-slate-800 rounded-2xl p-6">
                    <h3 className="text-white font-semibold mb-4">Strategic Goals 2025</h3>
                    <div className="space-y-4">
                        <div>
                            <div className="flex justify-between mb-2">
                                <span className="text-slate-300 text-sm font-medium">Overall Progress</span>
                                <span className="text-emerald-400 font-bold">{metrics?.strategic_initiatives_progress}%</span>
                            </div>
                            <div className="h-3 bg-slate-900 rounded-full overflow-hidden">
                                <div
                                    className="h-full bg-gradient-to-r from-red-600 to-red-400 transition-all duration-500"
                                    style={{ width: `${metrics?.strategic_initiatives_progress}%` }}
                                />
                            </div>
                        </div>
                        <div className="grid grid-cols-2 gap-3 mt-4">
                            <div className="p-3 bg-slate-900/50 rounded-lg text-center">
                                <p className="text-xs text-slate-400 mb-1">Revenue Target</p>
                                <p className="text-lg font-bold text-white">85%</p>
                            </div>
                            <div className="p-3 bg-slate-900/50 rounded-lg text-center">
                                <p className="text-xs text-slate-400 mb-1">Market Share</p>
                                <p className="text-lg font-bold text-emerald-400">+2.5%</p>
                            </div>
                            <div className="p-3 bg-slate-900/50 rounded-lg text-center">
                                <p className="text-xs text-slate-400 mb-1">Cost Reduction</p>
                                <p className="text-lg font-bold text-white">92%</p>
                            </div>
                            <div className="p-3 bg-slate-900/50 rounded-lg text-center">
                                <p className="text-xs text-slate-400 mb-1">Innovation</p>
                                <p className="text-lg font-bold text-purple-400">6 Projects</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            {/* Governance & Compliance */}
            <div className="bg-[#1e293b] border border-slate-800 rounded-2xl p-6">
                <h3 className="text-white font-semibold mb-4">Governance & Compliance</h3>
                <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                    <div className="p-4 bg-emerald-900/20 border border-emerald-500/30 rounded-lg">
                        <p className="text-emerald-400 text-xs font-bold uppercase mb-1">Audit Status</p>
                        <p className="text-white font-semibold">Compliant</p>
                    </div>
                    <div className="p-4 bg-blue-900/20 border border-blue-500/30 rounded-lg">
                        <p className="text-blue-400 text-xs font-bold uppercase mb-1">Risk Score</p>
                        <p className="text-white font-semibold">Low (2.8/10)</p>
                    </div>
                    <div className="p-4 bg-purple-900/20 border border-purple-500/30 rounded-lg">
                        <p className="text-purple-400 text-xs font-bold uppercase mb-1">Board Meetings</p>
                        <p className="text-white font-semibold">11/12</p>
                    </div>
                    <div className="p-4 bg-amber-900/20 border border-amber-500/30 rounded-lg">
                        <p className="text-amber-400 text-xs font-bold uppercase mb-1">Next Review</p>
                        <p className="text-white font-semibold">Jan 15, 2026</p>
                    </div>
                </div>
            </div>
        </div>
    );
}
