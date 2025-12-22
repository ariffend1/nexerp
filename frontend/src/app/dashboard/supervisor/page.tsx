'use client';

import { useState, useEffect } from 'react';
import api from '@/lib/api';
import KPICard from '@/components/dashboard/KPICard';
import { Target, Users, Package, AlertTriangle, TrendingUp } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

export default function SupervisorDashboard() {
    const [metrics, setMetrics] = useState<any>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchMetrics();
    }, []);

    const fetchMetrics = async () => {
        try {
            const response = await api.get('/dashboards/supervisor');
            setMetrics(response.data.metrics);
        } catch (error) {
            console.error('Error fetching Supervisor metrics:', error);
        } finally {
            setLoading(false);
        }
    };

    if (loading) {
        return (
            <div className="flex items-center justify-center min-h-screen">
                <div className="text-center">
                    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-amber-500 mx-auto mb-4"></div>
                    <p className="text-slate-400">Loading dashboard...</p>
                </div>
            </div>
        );
    }

    const productionData = [
        { day: 'Mon', actual: 45, target: 50 },
        { day: 'Tue', actual: 52, target: 50 },
        { day: 'Wed', actual: 48, target: 50 },
        { day: 'Thu', actual: 55, target: 50 },
        { day: 'Fri', actual: metrics?.production_today || 42, target: metrics?.production_target || 50 }
    ];

    return (
        <div className="space-y-6">
            {/* Header */}
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-3xl font-bold text-white mb-2">Supervisor Dashboard</h1>
                    <p className="text-slate-400">Daily Operations & Team Coordination</p>
                </div>
                <div className="flex items-center gap-3">
                    <span className="px-4 py-2 bg-amber-600/20 text-amber-400 rounded-lg border border-amber-500/30 text-sm font-medium">
                        {new Date().toLocaleDateString('id-ID', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })}
                    </span>
                </div>
            </div>

            {/* KPI Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <KPICard
                    title="Production Today"
                    value={`${metrics?.production_today}/${metrics?.production_target}`}
                    icon={Target}
                    color="amber"
                    subtitle="Units completed"
                />
                <KPICard
                    title="Team Attendance"
                    value={`${metrics?.team_attendance}/${metrics?.team_size}`}
                    icon={Users}
                    color="green"
                    trend={((metrics?.team_attendance / metrics?.team_size) * 100 - 90)}
                />
                <KPICard
                    title="Pending Work Orders"
                    value={metrics?.pending_work_orders || 0}
                    icon={Package}
                    color="blue"
                    subtitle="Scheduled"
                />
                <KPICard
                    title="Low Stock Items"
                    value={metrics?.low_stock_items || 0}
                    icon={AlertTriangle}
                    color="red"
                    subtitle="Need attention"
                />
            </div>

            {/* Main Content */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                {/* Production Chart */}
                <div className="lg:col-span-2 bg-[#1e293b] border border-slate-800 rounded-2xl p-6">
                    <h3 className="text-white font-semibold mb-4">Production vs Target (This Week)</h3>
                    <ResponsiveContainer width="100%" height={250}>
                        <BarChart data={productionData}>
                            <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                            <XAxis dataKey="day" stroke="#94a3b8" />
                            <YAxis stroke="#94a3b8" />
                            <Tooltip
                                contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #475569', borderRadius: '8px' }}
                                labelStyle={{ color: '#fff' }}
                            />
                            <Bar dataKey="actual" fill="#f59e0b" radius={[8, 8, 0, 0]} />
                            <Bar dataKey="target" fill="#475569" radius={[8, 8, 0, 0]} />
                        </BarChart>
                    </ResponsiveContainer>
                    <div className="flex justify-center gap-6 mt-4">
                        <div className="flex items-center gap-2">
                            <div className="w-3 h-3 bg-amber-500 rounded"></div>
                            <span className="text-xs text-slate-400">Actual</span>
                        </div>
                        <div className="flex items-center gap-2">
                            <div className="w-3 h-3 bg-slate-600 rounded"></div>
                            <span className="text-xs text-slate-400">Target</span>
                        </div>
                    </div>
                </div>

                {/* Quality Metrics */}
                <div className="bg-[#1e293b] border border-slate-800 rounded-2xl p-6">
                    <h3 className="text-white font-semibold mb-4">Quality Metrics</h3>
                    <div className="space-y-4">
                        <div>
                            <div className="flex justify-between mb-2">
                                <span className="text-slate-400 text-sm">Defect Rate</span>
                                <span className={`font-bold ${metrics?.defect_rate < 2 ? 'text-emerald-400' : 'text-amber-400'}`}>
                                    {metrics?.defect_rate}%
                                </span>
                            </div>
                            <div className="h-2 bg-slate-900 rounded-full overflow-hidden">
                                <div
                                    className={`h-full ${metrics?.defect_rate < 2 ? 'bg-emerald-500' : 'bg-amber-500'} transition-all`}
                                    style={{ width: `${metrics?.defect_rate * 10}%` }}
                                />
                            </div>
                            <p className="text-[10px] text-slate-500 mt-1">Target: &lt; 2%</p>
                        </div>
                        <div>
                            <div className="flex justify-between mb-2">
                                <span className="text-slate-400 text-sm">On-Time Delivery</span>
                                <span className="text-emerald-400 font-bold">{metrics?.on_time_delivery_rate}%</span>
                            </div>
                            <div className="h-2 bg-slate-900 rounded-full overflow-hidden">
                                <div
                                    className="h-full bg-emerald-500 transition-all"
                                    style={{ width: `${metrics?.on_time_delivery_rate}%` }}
                                />
                            </div>
                            <p className="text-[10px] text-slate-500 mt-1">Target: &gt; 95%</p>
                        </div>
                        <div className="mt-6 p-4 bg-emerald-900/20 border border-emerald-500/30 rounded-lg text-center">
                            <p className="text-emerald-400 text-xs font-bold uppercase mb-1">Overall Performance</p>
                            <p className="text-3xl font-bold text-white">A+</p>
                        </div>
                    </div>
                </div>
            </div>

            {/* Today's Tasks */}
            <div className="bg-[#1e293b] border border-slate-800 rounded-2xl p-6">
                <h3 className="text-white font-semibold mb-4">Today&apos;s Priority Tasks</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    {[
                        { task: 'Complete SPK-2512-0045', status: 'in_progress', priority: 'high' },
                        { task: 'Material request for Line 2', status: 'pending', priority: 'medium' },
                        { task: 'Quality inspection - Batch 789', status: 'pending', priority: 'high' },
                        { task: 'Team briefing at 14:00', status: 'scheduled', priority: 'low' },
                        { task: 'Update production report', status: 'in_progress', priority: 'medium' },
                        { task: 'Safety check - Equipment A3', status: 'pending', priority: 'high' }
                    ].map((item, idx) => (
                        <div key={idx} className={`p-4 rounded-lg border-l-4 ${item.priority === 'high' ? 'bg-red-900/20 border-red-500' :
                                item.priority === 'medium' ? 'bg-amber-900/20 border-amber-500' :
                                    'bg-blue-900/20 border-blue-500'
                            }`}>
                            <div className="flex items-start justify-between mb-2">
                                <p className="text-white text-sm font-medium">{item.task}</p>
                                <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold ${item.priority === 'high' ? 'bg-red-500/20 text-red-400' :
                                        item.priority === 'medium' ? 'bg-amber-500/20 text-amber-400' :
                                            'bg-blue-500/20 text-blue-400'
                                    }`}>
                                    {item.priority.toUpperCase()}
                                </span>
                            </div>
                            <p className="text-xs text-slate-500 capitalize">{item.status.replace('_', ' ')}</p>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
}
