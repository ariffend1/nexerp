'use client';

import { LucideIcon } from 'lucide-react';
import { ArrowUpRight, ArrowDownRight, Minus } from 'lucide-react';

interface KPICardProps {
    title: string;
    value: string | number;
    icon: LucideIcon;
    trend?: number;
    trendLabel?: string;
    color?: string;
    subtitle?: string;
}

export default function KPICard({
    title,
    value,
    icon: Icon,
    trend,
    trendLabel,
    color = 'blue',
    subtitle
}: KPICardProps) {
    const colorClasses = {
        blue: 'bg-blue-500/10 text-blue-400 border-blue-500/20',
        green: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20',
        amber: 'bg-amber-500/10 text-amber-400 border-amber-500/20',
        purple: 'bg-purple-500/10 text-purple-400 border-purple-500/20',
        red: 'bg-red-500/10 text-red-400 border-red-500/20',
        cyan: 'bg-cyan-500/10 text-cyan-400 border-cyan-500/20'
    };

    const getTrendColor = () => {
        if (!trend) return 'text-slate-500';
        if (trend > 0) return 'text-emerald-400';
        if (trend < 0) return 'text-red-400';
        return 'text-slate-500';
    };

    const TrendIcon = trend && trend > 0 ? ArrowUpRight : trend && trend < 0 ? ArrowDownRight : Minus;

    return (
        <div className="bg-[#1e293b] border border-slate-800 rounded-2xl p-6 hover:border-slate-700 transition-all group">
            <div className="flex justify-between items-start mb-4">
                <div className={`p-3 rounded-xl ${colorClasses[color as keyof typeof colorClasses]}`}>
                    <Icon className="w-6 h-6" />
                </div>
                {trend !== undefined && (
                    <div className={`flex items-center text-sm font-medium ${getTrendColor()}`}>
                        {trendLabel || (trend > 0 ? `+${trend}%` : `${trend}%`)}
                        <TrendIcon className="w-4 h-4 ml-1" />
                    </div>
                )}
            </div>
            <h3 className="text-slate-400 text-sm font-medium mb-2">{title}</h3>
            <p className="text-3xl font-bold text-white tracking-tight">{value}</p>
            {subtitle && <p className="text-xs text-slate-500 mt-2">{subtitle}</p>}
        </div>
    );
}
