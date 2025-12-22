'use client';

import { useState, useEffect } from 'react';
import api from '@/lib/api';
import KPICard from '@/components/dashboard/KPICard';
import { DollarSign, Briefcase, Users, CheckCircle, PieChart, BarChart } from 'lucide-react';
import { BarChart as RechartsBar, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart as RechartsPie, Pie, Cell } from 'recharts';

export default function ManagerDashboard() {
    const [metrics, setMetrics] = useState<any>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchMetrics();
    }, []);

    const fetchMetrics = async () => {
        try {
            const response = await api.get('/dashboards/manager');
            setMetrics(response.data.metrics);
        } catch (error) {
            console.error('Error fetching Manager metrics:', error);
        } finally {
            setLoading(false);
        }
    };

    if (loading) {
        return (
            <div className="flex items-center justify-center min-h-screen">
                <div className="text-center">
                    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-emerald-500 mx-auto mb-4"></div>
                    <p className="text-slate-400">Loading dashboard...</p>
                </div>
            </div>
        );
    }

    const budgetData = [
        { name: 'Spent', value: metrics?.budget_spent || 0, color: '#10b981' },
        { name: 'Remaining', value: metrics?.budget_remaining || 0, color: '#475569' }
    ];

    return (
        <div className="space-y-6">
            {/* Header */}
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-3xl font-bold text-white mb-2">Manager Dashboard</h1>
                    <p className="text-slate-400">Operational Performance & Team Metrics</p>
                </div>
                <button className="bg-emerald-600 hover:bg-emerald-500 text-white px-4 py-2 rounded-lg transition-all flex items-center gap-2">
                    <CheckCircle className="w-4 h-4" />
                    Approvals ({metrics?.pending_approvals})
                </button>
            </div>

            {/* KPI Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <KPICard
                    title="Revenue MTD"
                    value={`Rp ${(metrics?.revenue_mtd / 1000000).toFixed(1)}M`}
                    icon={DollarSign}
                    color="green"
                    trend={12.5}
                />
                <KPICard
                    title="Active Projects"
                    value={metrics?.active_projects || 0}
                    icon={Briefcase}
                    color="blue"
                    subtitle="In progress"
                />
                <KPICard
                    title="Team Size"
                    value={metrics?.total_employees || 0}
                    icon={Users}
                    color="purple"
                    trend={3}
                />
                <KPICard
                    title="Productivity"
                    value={`${metrics?.productivity_score}%`}
                    icon={BarChart}
                    color="amber"
                    trend={5.2}
                />
            </div>

            {/* Main Content */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                {/* Budget Tracking */}
                <div className="lg:col-span-2 bg-[#1e293b] border border-slate-800 rounded-2xl p-6">
                    <h3 className="text-white font-semibold mb-4">Budget Overview</h3>
                    <div className="grid grid-cols-3 gap-4 mb-6">
                        <div className="text-center p-4 bg-slate-900/50 rounded-lg">
                            <p className="text-slate-400 text-xs mb-1">Allocated</p>
                            <p className="text-2xl font-bold text-white">Rp {(metrics?.budget_allocated / 1000000).toFixed(1)}M</p>
                        </div>
                        <div className="text-center p-4 bg-emerald-900/20 border border-emerald-500/30 rounded-lg">
                            <p className="text-emerald-400 text-xs mb-1">Spent</p>
                            <p className="text-2xl font-bold text-emerald-400">Rp {(metrics?.budget_spent / 1000000).toFixed(1)}M</p>
                        </div>
                        <div className="text-center p-4 bg-slate-900/50 rounded-lg">
                            <p className="text-slate-400 text-xs mb-1">Remaining</p>
                            <p className="text-2xl font-bold text-white">Rp {(metrics?.budget_remaining / 1000000).toFixed(1)}M</p>
                        </div>
                    </div>
                    <div className="h-4 bg-slate-900 rounded-full overflow-hidden">
                        <div
                            className="h-full bg-emerald-500 transition-all duration-500"
                            style={{ width: `${(metrics?.budget_spent / metrics?.budget_allocated * 100)}%` }}
                        />
                    </div>
                    <p className="text-xs text-slate-500 mt-2">
                        {(metrics?.budget_spent / metrics?.budget_allocated * 100).toFixed(1)}% of budget utilized
                    </p>
                </div>

                {/* Pending Approvals */}
                <div className="bg-[#1e293b] border border-slate-800 rounded-2xl p-6">
                    <h3 className="text-white font-semibold mb-4">Pending Approvals</h3>
                    <div className="space-y-3">
                        {[
                            { type: 'Purchase Order', count: 3, color: 'blue' },
                            { type: 'Leave Request', count: 2, color: 'amber' },
                            { type: 'Expense Claim', count: 5, color: 'purple' },
                            { type: 'Budget Request', count: 1, color: 'emerald' }
                        ].map((item) => (
                            <div key={item.type} className="flex items-center justify-between p-3 bg-slate-900/50 rounded-lg hover:bg-slate-800/50 transition-colors cursor-pointer">
                                <span className="text-slate-300 text-sm">{item.type}</span>
                                <span className={`px-2 py-1 bg-${item.color}-500/10 text-${item.color}-400 text-xs font-bold rounded-full`}>
                                    {item.count}
                                </span>
                            </div>
                        ))}
                    </div>
                    <button className="w-full mt-4 bg-emerald-600 hover:bg-emerald-500 text-white py-2 rounded-lg transition-all">
                        View All
                    </button>
                </div>
            </div>

            {/* Team Performance */}
            <div className="bg-[#1e293b] border border-slate-800 rounded-2xl p-6">
                <h3 className="text-white font-semibold mb-4">Team Performance</h3>
                <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                    {[
                        { name: 'Sales Team', score: 92, target: 90 },
                        { name: 'Production', score: 88, target: 85 },
                        { name: 'Procurement', score: 95, target: 90 },
                        { name: 'Finance', score: 90, target: 88 }
                    ].map((team) => (
                        <div key={team.name} className="p-4 bg-slate-900/50 rounded-lg">
                            <div className="flex justify-between mb-2">
                                <span className="text-slate-300 text-sm font-medium">{team.name}</span>
                                <span className={`text-sm font-bold ${team.score >= team.target ? 'text-emerald-400' : 'text-amber-400'}`}>
                                    {team.score}%
                                </span>
                            </div>
                            <div className="h-2 bg-slate-900 rounded-full overflow-hidden">
                                <div
                                    className={`h-full ${team.score >= team.target ? 'bg-emerald-500' : 'bg-amber-500'} transition-all duration-500`}
                                    style={{ width: `${team.score}%` }}
                                />
                            </div>
                            <p className="text-[10px] text-slate-500 mt-1">Target: {team.target}%</p>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
}
