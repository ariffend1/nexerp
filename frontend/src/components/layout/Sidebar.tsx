'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import {
    BarChart3,
    Box,
    Briefcase,
    Calculator,
    Factory,
    LayoutDashboard,
    Package,
    Settings,
    ShoppingCart,
    Truck,
    Users
} from 'lucide-react';
import { cn } from '@/lib/utils';

const menuItems = [
    { icon: LayoutDashboard, label: 'Dashboard', href: '/dashboard' },
    { icon: Factory, label: 'Manufacturing', href: '/dashboard/manufacturing' },
    { icon: Briefcase, label: 'Projects', href: '/dashboard/projects' },
    { icon: ShoppingCart, label: 'Procurement', href: '/dashboard/procurement' },
    { icon: Truck, label: 'Sales & Distribution', href: '/dashboard/sales' },
    { icon: Box, label: 'Inventory', href: '/dashboard/inventory' },
    { icon: Calculator, label: 'Accounting', href: '/dashboard/accounting' },
    { icon: Users, label: 'Employees', href: '/dashboard/employees' },
    { icon: Package, label: 'Cash & Bank', href: '/dashboard/cash-bank' },
    { icon: Users, label: 'Partners', href: '/dashboard/partners' },
    { icon: BarChart3, label: 'Approvals', href: '/dashboard/approvals' },
    { icon: BarChart3, label: 'Reports', href: '/dashboard/reports' },
    { icon: Settings, label: 'Settings', href: '/dashboard/settings' },
];

export default function Sidebar() {
    const pathname = usePathname();

    return (
        <aside className="fixed left-0 top-0 h-screen w-64 bg-[#0f172a] border-r border-slate-800 flex flex-col z-50">
            <div className="p-6">
                <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-400 to-indigo-500 bg-clip-text text-transparent">
                    NexERP
                </h1>
            </div>

            <nav className="flex-1 px-4 py-4 space-y-1 overflow-y-auto">
                {menuItems.map((item) => (
                    <Link
                        key={item.href}
                        href={item.href}
                        className={cn(
                            "flex items-center gap-3 px-4 py-3 rounded-xl transition-all group",
                            pathname === item.href
                                ? "bg-blue-600 text-white shadow-lg shadow-blue-500/20"
                                : "text-slate-400 hover:bg-slate-800 hover:text-white"
                        )}
                    >
                        <item.icon className={cn(
                            "w-5 h-5 transition-colors",
                            pathname === item.href ? "text-white" : "text-slate-500 group-hover:text-blue-400"
                        )} />
                        <span className="font-medium">{item.label}</span>
                    </Link>
                ))}
            </nav>

            <div className="p-4 border-t border-slate-800">
                <div className="flex items-center gap-3 px-4 py-2">
                    <div className="w-8 h-8 rounded-full bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center text-xs font-bold text-white uppercase text-center">
                        AD
                    </div>
                    <div className="flex-1 overflow-hidden">
                        <p className="text-sm font-medium text-white truncate">Admin User</p>
                        <p className="text-xs text-slate-500 truncate">Workspace Alpha</p>
                    </div>
                </div>
            </div>
        </aside>
    );
}
