'use client';

import {
    Package,
    ShoppingCart,
    Clock,
    Factory,
    ArrowUpRight,
    ArrowDownRight,
    Briefcase
} from 'lucide-react';

const stats = [
    { label: 'Active Projects', value: '12', icon: Clock, color: 'text-blue-400', trend: '+2', trendUp: true },
    { label: 'Production Orders', value: '45', icon: Factory, color: 'text-indigo-400', trend: '+5', trendUp: true },
    { label: 'Inventory Value', value: '$240k', icon: Package, color: 'text-emerald-400', trend: '-2%', trendUp: false },
    { label: 'Pending POs', value: '8', icon: ShoppingCart, color: 'text-amber-400', trend: 'Stable', trendUp: true },
];

export default function DashboardPage() {
    return (
        <div className="space-y-8">
            <div>
                <h2 className="text-3xl font-bold text-white mb-2">Welcome Back, Admin</h2>
                <p className="text-slate-400">Here&apos;s what&apos;s happening in your workspace today.</p>
            </div>

            {/* Stats Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                {stats.map((stat) => (
                    <div key={stat.label} className="bg-[#1e293b] border border-slate-800 p-6 rounded-2xl hover:border-slate-700 transition-all group">
                        <div className="flex justify-between items-start mb-4">
                            <div className={`p-2 rounded-xl bg-slate-900 overflow-hidden ${stat.color}`}>
                                <stat.icon className="w-6 h-6" />
                            </div>
                            <div className={`flex items-center text-xs font-medium ${stat.trendUp ? 'text-emerald-400' : 'text-red-400'}`}>
                                {stat.trend}
                                {stat.trendUp ? <ArrowUpRight className="w-3 h-3 ml-1" /> : <ArrowDownRight className="w-3 h-3 ml-1" />}
                            </div>
                        </div>
                        <h3 className="text-slate-400 text-sm font-medium mb-1">{stat.label}</h3>
                        <p className="text-2xl font-bold text-white tracking-tight">{stat.value}</p>
                    </div>
                ))}
            </div>

            {/* Main Grid Sections */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                {/* Recent Production Section */}
                <div className="lg:col-span-2 bg-[#1e293b] border border-slate-800 rounded-2xl p-6">
                    <div className="flex justify-between items-center mb-6">
                        <h3 className="text-lg font-semibold text-white">Recent Production Orders</h3>
                        <button className="text-blue-400 text-sm hover:underline">View All</button>
                    </div>
                    <div className="space-y-4">
                        {[1, 2, 3].map((i) => (
                            <div key={i} className="flex items-center justify-between p-4 bg-slate-900/50 rounded-xl border border-slate-800/50">
                                <div className="flex items-center gap-4">
                                    <div className="w-10 h-10 rounded-lg bg-blue-500/10 flex items-center justify-center text-blue-400 font-bold">#JO</div>
                                    <div>
                                        <h4 className="text-sm font-medium text-white">SPK-2512-000{i}</h4>
                                        <p className="text-xs text-slate-500">Aluminum Frame Assembly</p>
                                    </div>
                                </div>
                                <div className="text-right">
                                    <span className="px-3 py-1 bg-amber-500/10 text-amber-400 text-[10px] font-bold uppercase rounded-full border border-amber-500/20">
                                        In Progress
                                    </span>
                                    <p className="text-xs text-slate-500 mt-1">Due: Dec 24, 2025</p>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Quick Actions / Alerts Section */}
                <div className="bg-[#1e293b] border border-slate-800 rounded-2xl p-6">
                    <h3 className="text-lg font-semibold text-white mb-6">Quick Actions</h3>
                    <div className="grid grid-cols-1 gap-3">
                        <a href="/dashboard/manufacturing" className="w-full text-left p-4 bg-slate-900 hover:bg-slate-800 rounded-xl border border-slate-800 transition-colors flex items-center gap-3">
                            <div className="p-2 bg-blue-500/10 rounded-lg text-blue-400">
                                <Package className="w-5 h-5" />
                            </div>
                            <div>
                                <p className="text-sm font-medium text-white">New Production Order</p>
                                <p className="text-xs text-slate-500">Standard SPK creation</p>
                            </div>
                        </a>
                        <a href="/dashboard/procurement" className="w-full text-left p-4 bg-slate-900 hover:bg-slate-800 rounded-xl border border-slate-800 transition-colors flex items-center gap-3">
                            <div className="p-2 bg-emerald-500/10 rounded-lg text-emerald-400">
                                <ShoppingCart className="w-5 h-5" />
                            </div>
                            <div>
                                <p className="text-sm font-medium text-white">Create Purchase Order</p>
                                <p className="text-xs text-slate-500">Inventory replenishment</p>
                            </div>
                        </a>
                        <a href="/dashboard/projects" className="w-full text-left p-4 bg-slate-900 hover:bg-slate-800 rounded-xl border border-slate-800 transition-colors flex items-center gap-3">
                            <div className="p-2 bg-indigo-500/10 rounded-lg text-indigo-400">
                                <Briefcase className="w-5 h-5" />
                            </div>
                            <div>
                                <p className="text-sm font-medium text-white">New Service Project</p>
                                <p className="text-xs text-slate-500">Task & Timeline tracking</p>
                            </div>
                        </a>
                    </div>
                </div>
            </div>
        </div>
    );
}
