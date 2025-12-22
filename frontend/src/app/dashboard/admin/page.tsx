'use client';

import { useState, useEffect } from 'react';
import api from '@/lib/api';
import KPICard from '@/components/dashboard/KPICard';
import { Users, Database, Zap, AlertCircle, Server, Activity } from 'lucide-react';

export default function AdminDashboard() {
    const [metrics, setMetrics] = useState<any>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchMetrics();
    }, []);

    const fetchMetrics = async () => {
        try {
            const response = await api.get('/dashboards/admin');
            setMetrics(response.data.metrics);
        } catch (error) {
            console.error('Error fetching Admin metrics:', error);
        } finally {
            setLoading(false);
        }
    };

    if (loading) {
        return (
            <div className="flex items-center justify-center min-h-screen">
                <div className="text-center">
                    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
                    <p className="text-slate-400">Loading system dashboard...</p>
                </div>
            </div>
        );
    }

    return (
        <div className="space-y-6">
            {/* Header */}
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-3xl font-bold text-white mb-2">Admin Dashboard</h1>
                    <p className="text-slate-400">System Health & User Management</p>
                </div>
                <div className="flex items-center gap-2 px-4 py-2 bg-emerald-900/20 border border-emerald-500/30 rounded-lg">
                    <div className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse"></div>
                    <span className="text-emerald-400 text-sm font-medium">All Systems Operational</span>
                </div>
            </div>

            {/* KPI Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <KPICard
                    title="Total Users"
                    value={`${metrics?.active_users}/${metrics?.total_users}`}
                    icon={Users}
                    color="blue"
                    subtitle="Active users"
                />
                <KPICard
                    title="API Requests Today"
                    value={metrics?.api_requests_today?.toLocaleString() || 0}
                    icon={Zap}
                    color="yellow"
                    trend={15}
                />
                <KPICard
                    title="Database Size"
                    value={`${metrics?.storage_used_gb} GB`}
                    icon={Database}
                    color="purple"
                    subtitle={`${metrics?.total_records} records`}
                />
                <KPICard
                    title="Error Count"
                    value={metrics?.error_count || 0}
                    icon={AlertCircle}
                    color={metrics?.error_count > 0 ? 'red' : 'green'}
                    subtitle="Last 24h"
                />
            </div>

            {/* System Performance */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Performance Metrics */}
                <div className="bg-[#1e293b] border border-slate-800 rounded-2xl p-6">
                    <h3 className="text-white font-semibold mb-4">Performance Metrics</h3>
                    <div className="space-y-4">
                        <div>
                            <div className="flex justify-between mb-2">
                                <span className="text-slate-400 text-sm">System Uptime</span>
                                <span className="text-emerald-400 font-bold">{metrics?.system_uptime}</span>
                            </div>
                            <div className="h-2 bg-slate-900 rounded-full overflow-hidden">
                                <div className="h-full bg-emerald-500" style={{ width: '99.98%' }} />
                            </div>
                        </div>
                        <div>
                            <div className="flex justify-between mb-2">
                                <span className="text-slate-400 text-sm">Avg Response Time</span>
                                <span className="text-blue-400 font-bold">{metrics?.avg_response_time_ms}ms</span>
                            </div>
                            <div className="h-2 bg-slate-900 rounded-full overflow-hidden">
                                <div className="h-full bg-blue-500" style={{ width: '75%' }} />
                            </div>
                            <p className="text-[10px] text-slate-500 mt-1">Target: &lt; 200ms</p>
                        </div>
                        <div className="grid grid-cols-2 gap-3 mt-6">
                            <div className="p-3 bg-slate-900/50 rounded-lg text-center">
                                <Server className="w-5 h-5 text-blue-400 mx-auto mb-1" />
                                <p className="text-xs text-slate-400 mb-1">CPU Usage</p>
                                <p className="text-lg font-bold text-white">45%</p>
                            </div>
                            <div className="p-3 bg-slate-900/50 rounded-lg text-center">
                                <Activity className="w-5 h-5 text-emerald-400 mx-auto mb-1" />
                                <p className="text-xs text-slate-400 mb-1">Memory</p>
                                <p className="text-lg font-bold text-white">2.1GB</p>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Recent Activities */}
                <div className="bg-[#1e293b] border border-slate-800 rounded-2xl p-6">
                    <h3 className="text-white font-semibold mb-4">Recent System Events</h3>
                    <div className="space-y-3">
                        {[
                            { event: 'Database backup completed', time: '5 min ago', type: 'success' },
                            { event: 'New user registration: john@example.com', time: '12 min ago', type: 'info' },
                            { event: 'System update applied successfully', time: '1 hour ago', type: 'success' },
                            { event: 'Failed login attempt detected', time: '2 hours ago', type: 'warning' },
                            { event: 'API rate limit hit: /api/products', time: '3 hours ago', type: 'warning' }
                        ].map((item, idx) => (
                            <div key={idx} className="flex items-start gap-3 p-3 bg-slate-900/50 rounded-lg hover:bg-slate-800/50 transition-colors">
                                <div className={`w-2 h-2 rounded-full mt-1.5 flex-shrink-0 ${item.type === 'success' ? 'bg-emerald-500' :
                                        item.type === 'warning' ? 'bg-amber-500' :
                                            'bg-blue-500'
                                    }`} />
                                <div className="flex-1 min-w-0">
                                    <p className="text-sm text-white">{item.event}</p>
                                    <p className="text-xs text-slate-500 mt-0.5">{item.time}</p>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>

            {/* Module Usage */}
            <div className="bg-[#1e293b] border border-slate-800 rounded-2xl p-6">
                <h3 className="text-white font-semibold mb-4">Module Usage Statistics</h3>
                <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4">
                    {[
                        { module: 'Procurement', usage: 85, color: 'emerald' },
                        { module: 'Sales', usage: 92, color: 'blue' },
                        { module: 'Manufacturing', usage: 78, color: 'purple' },
                        { module: 'Inventory', usage: 95, color: 'amber' },
                        { module: 'Finance', usage: 88, color: 'cyan' },
                        { module: 'HR', usage: 65, color: 'pink' }
                    ].map((item) => (
                        <div key={item.module} className="p-4 bg-slate-900/50 rounded-lg">
                            <p className="text-xs text-slate-400 mb-2">{item.module}</p>
                            <p className={`text-2xl font-bold text-${item.color}-400`}>{item.usage}%</p>
                            <div className="h-1 bg-slate-900 rounded-full mt-2 overflow-hidden">
                                <div
                                    className={`h-full bg-${item.color}-500 transition-all`}
                                    style={{ width: `${item.usage}%` }}
                                />
                            </div>
                        </div>
                    ))}
                </div>
            </div>

            {/* Quick Actions */}
            <div className="bg-[#1e293b] border border-slate-800 rounded-2xl p-6">
                <h3 className="text-white font-semibold mb-4">Admin Actions</h3>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                    <button className="p-4 bg-blue-600 hover:bg-blue-500 text-white rounded-lg transition-all text-sm font-medium">
                        User Management
                    </button>
                    <button className="p-4 bg-purple-600 hover:bg-purple-500 text-white rounded-lg transition-all text-sm font-medium">
                        System Settings
                    </button>
                    <button className="p-4 bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg transition-all text-sm font-medium">
                        Backup Database
                    </button>
                    <button className="p-4 bg-amber-600 hover:bg-amber-500 text-white rounded-lg transition-all text-sm font-medium">
                        View Audit Logs
                    </button>
                </div>
            </div>
        </div>
    );
}
