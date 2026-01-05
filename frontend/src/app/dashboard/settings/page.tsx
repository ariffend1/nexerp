'use client';

import { User, Building2, Shield, Bell, Palette, Database, Key } from 'lucide-react';

const settingsSections = [
    {
        title: 'Profile Settings',
        icon: User,
        description: 'Update your personal information and preferences',
        items: ['Name & Email', 'Password', 'Two-Factor Auth']
    },
    {
        title: 'Company Settings',
        icon: Building2,
        description: 'Configure company details and branding',
        items: ['Company Info', 'Logo & Branding', 'Address & Contact']
    },
    {
        title: 'User Management',
        icon: Shield,
        description: 'Manage users, roles, and permissions',
        items: ['Users', 'Roles', 'Permissions']
    },
    {
        title: 'Notifications',
        icon: Bell,
        description: 'Configure email and system notifications',
        items: ['Email Alerts', 'Push Notifications', 'Digest Settings']
    },
    {
        title: 'Appearance',
        icon: Palette,
        description: 'Customize the look and feel',
        items: ['Theme', 'Language', 'Date Format']
    },
    {
        title: 'Data & Backup',
        icon: Database,
        description: 'Manage data exports and backups',
        items: ['Export Data', 'Import Data', 'Backup Schedule']
    },
    {
        title: 'API Keys',
        icon: Key,
        description: 'Manage API access and integrations',
        items: ['API Keys', 'Webhooks', 'Integrations']
    },
];

export default function SettingsPage() {
    return (
        <div className="space-y-6">
            <div>
                <h2 className="text-2xl font-bold text-white">Settings</h2>
                <p className="text-slate-400 text-sm">Manage your account and workspace settings</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {settingsSections.map((section) => (
                    <button
                        key={section.title}
                        onClick={() => alert(`${section.title} - Coming Soon`)}
                        className="bg-[#1e293b] border border-slate-800 rounded-2xl p-6 text-left hover:border-slate-700 transition-all group"
                    >
                        <div className="flex items-start gap-4">
                            <div className="p-3 bg-slate-900 rounded-xl text-blue-400 group-hover:bg-blue-500/10 transition-colors">
                                <section.icon className="w-6 h-6" />
                            </div>
                            <div className="flex-1">
                                <h3 className="text-lg font-semibold text-white mb-1">{section.title}</h3>
                                <p className="text-sm text-slate-500 mb-3">{section.description}</p>
                                <div className="flex flex-wrap gap-2">
                                    {section.items.map((item) => (
                                        <span
                                            key={item}
                                            className="text-[10px] px-2 py-1 bg-slate-800 text-slate-400 rounded-full uppercase font-medium"
                                        >
                                            {item}
                                        </span>
                                    ))}
                                </div>
                            </div>
                        </div>
                    </button>
                ))}
            </div>

            {/* Workspace Info */}
            <div className="bg-[#1e293b] border border-slate-800 rounded-2xl p-6">
                <h3 className="text-lg font-semibold text-white mb-4">Current Workspace</h3>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <div>
                        <p className="text-slate-500 text-xs font-bold uppercase mb-1">Workspace Name</p>
                        <p className="text-white font-medium">Default</p>
                    </div>
                    <div>
                        <p className="text-slate-500 text-xs font-bold uppercase mb-1">Plan</p>
                        <p className="text-white font-medium">Enterprise</p>
                    </div>
                    <div>
                        <p className="text-slate-500 text-xs font-bold uppercase mb-1">Users</p>
                        <p className="text-white font-medium">1 / Unlimited</p>
                    </div>
                </div>
            </div>
        </div>
    );
}
