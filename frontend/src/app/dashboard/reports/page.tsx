'use client';

import { FileText, Download, Calendar, TrendingUp, DollarSign, Package, Users } from 'lucide-react';
import { cn } from '@/lib/utils';

const reportCategories = [
    {
        title: 'Financial Reports',
        icon: DollarSign,
        color: 'text-emerald-400',
        bgColor: 'bg-emerald-500/10',
        reports: [
            { name: 'Profit & Loss Statement', path: '/reports/pnl' },
            { name: 'Balance Sheet', path: '/reports/balance-sheet' },
            { name: 'Cash Flow Statement', path: '/reports/cash-flow' },
            { name: 'General Ledger', path: '/reports/general-ledger' },
        ]
    },
    {
        title: 'Sales Reports',
        icon: TrendingUp,
        color: 'text-blue-400',
        bgColor: 'bg-blue-500/10',
        reports: [
            { name: 'Sales Summary', path: '/reports/sales-summary' },
            { name: 'Sales by Customer', path: '/reports/sales-by-customer' },
            { name: 'Sales by Product', path: '/reports/sales-by-product' },
            { name: 'Aging Report', path: '/reports/aging' },
        ]
    },
    {
        title: 'Inventory Reports',
        icon: Package,
        color: 'text-indigo-400',
        bgColor: 'bg-indigo-500/10',
        reports: [
            { name: 'Stock Summary', path: '/reports/stock-summary' },
            { name: 'Stock Movement', path: '/reports/stock-movement' },
            { name: 'Stock Valuation', path: '/reports/stock-valuation' },
            { name: 'Reorder Report', path: '/reports/reorder' },
        ]
    },
    {
        title: 'HR Reports',
        icon: Users,
        color: 'text-amber-400',
        bgColor: 'bg-amber-500/10',
        reports: [
            { name: 'Employee Directory', path: '/reports/employees' },
            { name: 'Payroll Summary', path: '/reports/payroll' },
            { name: 'Attendance Report', path: '/reports/attendance' },
            { name: 'Leave Report', path: '/reports/leave' },
        ]
    },
];

export default function ReportsPage() {
    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <div>
                    <h2 className="text-2xl font-bold text-white">Reports</h2>
                    <p className="text-slate-400 text-sm">Generate and export business reports</p>
                </div>
                <div className="flex gap-2">
                    <button className="bg-slate-800 hover:bg-slate-700 text-white px-4 py-2 rounded-lg flex items-center gap-2 transition-all">
                        <Calendar className="w-4 h-4" />
                        Date Range
                    </button>
                </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {reportCategories.map((category) => (
                    <div key={category.title} className="bg-[#1e293b] border border-slate-800 rounded-2xl overflow-hidden">
                        <div className="p-4 border-b border-slate-800 flex items-center gap-3 bg-slate-900/20">
                            <div className={cn("p-2 rounded-lg", category.bgColor)}>
                                <category.icon className={cn("w-5 h-5", category.color)} />
                            </div>
                            <h3 className="text-lg font-semibold text-white">{category.title}</h3>
                        </div>
                        <div className="p-4 space-y-2">
                            {category.reports.map((report) => (
                                <button
                                    key={report.name}
                                    onClick={() => alert(`${report.name} - Coming Soon`)}
                                    className="w-full text-left p-3 bg-slate-900/50 hover:bg-slate-800 rounded-lg border border-slate-800/50 transition-colors flex items-center justify-between group"
                                >
                                    <div className="flex items-center gap-3">
                                        <FileText className="w-4 h-4 text-slate-500" />
                                        <span className="text-sm text-slate-300 group-hover:text-white">{report.name}</span>
                                    </div>
                                    <Download className="w-4 h-4 text-slate-600 group-hover:text-blue-400" />
                                </button>
                            ))}
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}
