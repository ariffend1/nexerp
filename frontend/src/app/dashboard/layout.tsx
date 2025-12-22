'use client';

import Sidebar from '@/components/layout/Sidebar';
import NotificationBell from '@/components/layout/NotificationBell';
import { Search, HelpCircle } from 'lucide-react';

export default function DashboardLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    return (
        <div className="min-h-screen bg-[#0b0f19]">
            <Sidebar />

            <main className="pl-64">
                {/* Navbar */}
                <header className="h-16 border-b border-slate-800 bg-[#0f172a]/50 backdrop-blur-md flex items-center justify-between px-8 sticky top-0 z-40">
                    <div className="flex items-center gap-4 w-96">
                        <div className="relative w-full">
                            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" />
                            <input
                                type="text"
                                placeholder="Search everything..."
                                className="w-full bg-slate-900/50 border border-slate-700 rounded-lg py-1.5 pl-10 pr-4 text-sm text-white focus:ring-1 focus:ring-blue-500 outline-none transition-all"
                            />
                        </div>
                    </div>

                    <div className="flex items-center gap-6">
                        <NotificationBell />
                        <button className="text-slate-400 hover:text-white transition-colors">
                            <HelpCircle className="w-5 h-5" />
                        </button>
                    </div>
                </header>

                {/* Content Area */}
                <div className="p-8">
                    {children}
                </div>
            </main>
        </div>
    );
}
