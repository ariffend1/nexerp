'use client';

import { useState, useEffect } from 'react';
import api from '@/lib/api';
import KPICard from '@/components/dashboard/KPICard';
import { TrendingUp, DollarSign, Users, Target, PieChart, BarChart3 } from 'lucide-react';
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';

export default function GMDashboard() {
    const [metrics, setMetrics] = useState<any>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchMetrics();
    }, []);

    const fetchMetrics = async () => {
        try {
            const response = await api.get('/dashboards/gm');
            setMetrics(response.data.metrics);
        } catch (error) {
            console.error('Error fetching GM metrics:', error);
        } finally {
            setLoading(false);
        }
    };

    if (loading) {
        return (
            <div className="flex items-center justify-center min-h-screen">
                <div className="text-center">
                    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-500 mx-auto mb-4"></div>
                    <p className="text-slate-400">Loading dashboard...</p>
                </div>
            </div>
        );
    }

    const revenueData = metrics?.monthly_revenue ? Object.entries(metrics.monthly_revenue).map(([month, value]) => ({
        month,
        revenue: value
    })) : [];

    return (
        <div className="space-y-6">
            {/* Header */}
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-3xl font-bold text-white mb-2">GM Dashboard</h1>
                    <p className="text-slate-400">Strategic Overview & Business Health</p>
                </div>
                <div className="flex items-center gap-3">
                    <button className="bg-purple-600 hover:bg-purple-500 text-white px-4 py-2 rounded-lg transition-all flex items-center gap-2">
                        <PieChart className="w-4 h-4" />
                        Strategic View
                    </button>
                    <button className="bg-slate-800 hover:bg-slate-700 text-white px-4 py-2 rounded-lg transition-all">
                        Export Report
                    </button>
                </div>
            </div>

            {/* KPI Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <KPICard
                    title="Revenue (6M)"
                    value={`Rp ${(metrics?.total_revenue_6m / 1000000).toFixed(1)}M`}
                    icon={DollarSign}
                    color="purple"
                    trend={12.5}
                />
                <KPICard
                    title="Gross Profit Margin"
                    value={`${metrics?.gross_profit_margin}%`}
                    icon={TrendingUp}
                    color="green"
                    subtitle="Target: 35%"
                />
                <KPICard
                    title="Cash Flow"
                    value={`Rp ${(metrics?.operating_cash_flow / 1000000).toFixed(1)}M`}
                    icon={BarChart3}
                    color="cyan"
                    trend={metrics?.operating_cash_flow > 0 ? 8 : -5}
                />
                <KPICard
                    title="Total Customers"
                    value={metrics?.customer_count || 0}
                    icon={Users}
                    color="purple"
                    trend={15}
                />
            </div>

            {/* Charts Row */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Revenue Trend */}
                <div className="bg-[#1e293b] border border-slate-800 rounded-2xl p-6">
                    <h3 className="text-white font-semibold mb-4">Revenue Trend (6 Months)</h3>
                    <ResponsiveContainer width="100%" height={250}>
                        <LineChart data={revenueData}>
                            <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                            <XAxis dataKey="month" stroke="#94a3b8" />
                            <YAxis stroke="#94a3b8" />
                            <Tooltip
                                contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #475569', borderRadius: '8px' }}
                                labelStyle={{ color: '#fff' }}
                            />
                            <Line
                                type="monotone"
                                dataKey="revenue"
                                stroke="#a855f7"
                                strokeWidth={3}
                                dot={{ fill: '#a855f7', r: 5 }}
                            />
                        </LineChart>
                    </ResponsiveContainer>
                </div>

                {/* Key Metrics */}
                <div className="bg-[#1e293b] border border-slate-800 rounded-2xl p-6">
                    <h3 className="text-white font-semibold mb-4">Key Business Metrics</h3>
                    <div className="space-y-4">
                        <div className="flex justify-between items-center p-3 bg-slate-900/50 rounded-lg">
                            <span className="text-slate-400 text-sm">Employee Turnover</span>
                            <span className="text-white font-bold">{metrics?.employee_turnover_rate}%</span>
                        </div>
                        <div className="flex justify-between items-center p-3 bg-slate-900/50 rounded-lg">
                            <span className="text-slate-400 text-sm">Market Share</span>
                            <span className="text-white font-bold">{metrics?.market_share}%</span>
                        </div>
                        <div className="flex justify-between items-center p-3 bg-slate-900/50 rounded-lg">
                            <span className="text-slate-400 text-sm">Customer Satisfaction</span>
                            <span className="text-emerald-400 font-bold">4.6/5.0</span>
                        </div>
                        <div className="flex justify-between items-center p-3 bg-slate-900/50 rounded-lg">
                            <span className="text-slate-400 text-sm">Net Promoter Score</span>
                            <span className="text-emerald-400 font-bold">+45</span>
                        </div>
                    </div>
                </div>
            </div>

            {/* Strategic Initiatives */}
            <div className="bg-[#1e293b] border border-slate-800 rounded-2xl p-6">
                <h3 className="text-white font-semibold mb-4">Strategic Initiatives</h3>
                <div className="space-y-4">
                    {[
                        { name: 'Digital Transformation', progress: 85, color: 'bg-purple-500' },
                        { name: 'Market Expansion', progress: 60, color: 'bg-blue-500' },
                        { name: 'Cost Optimization', progress: 75, color: 'bg-emerald-500' },
                        { name: 'Product Innovation', progress: 40, color: 'bg-amber-500' }
                    ].map((initiative) => (
                        <div key={initiative.name}>
                            <div className="flex justify-between mb-2">
                                <span className="text-sm text-slate-400">{initiative.name}</span>
                                <span className="text-sm font-medium text-white">{initiative.progress}%</span>
                            </div>
                            <div className="h-2 bg-slate-900 rounded-full overflow-hidden">
                                <div
                                    className={`h-full ${initiative.color} transition-all duration-500`}
                                    style={{ width: `${initiative.progress}%` }}
                                />
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
}
