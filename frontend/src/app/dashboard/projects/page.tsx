'use client';

import { useState, useEffect } from 'react';
import { Briefcase, Plus, Search } from 'lucide-react';

export default function ProjectsPage() {
    const [projects, setProjects] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchProjects = async () => {
            try {
                // Placeholder - can be connected to actual API later
                setProjects([]);
            } catch (error) {
                console.error('Error fetching projects:', error);
            } finally {
                setLoading(false);
            }
        };
        fetchProjects();
    }, []);

    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <div>
                    <h2 className="text-2xl font-bold text-white">Projects</h2>
                    <p className="text-slate-400 text-sm">Manage service projects and tasks</p>
                </div>
                <button
                    onClick={() => alert('Create Project - Coming Soon')}
                    className="bg-blue-600 hover:bg-blue-500 text-white px-4 py-2 rounded-lg flex items-center gap-2 transition-all shadow-lg shadow-blue-500/20"
                >
                    <Plus className="w-4 h-4" />
                    New Project
                </button>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-4 gap-6 mb-8">
                <div className="bg-[#1e293b] p-4 rounded-xl border border-slate-800">
                    <p className="text-slate-500 text-xs font-bold uppercase mb-1">Active Projects</p>
                    <p className="text-xl font-bold text-white">0</p>
                </div>
                <div className="bg-[#1e293b] p-4 rounded-xl border border-slate-800">
                    <p className="text-slate-500 text-xs font-bold uppercase mb-1">In Progress</p>
                    <p className="text-xl font-bold text-white">0</p>
                </div>
                <div className="bg-[#1e293b] p-4 rounded-xl border border-slate-800">
                    <p className="text-slate-500 text-xs font-bold uppercase mb-1">Completed</p>
                    <p className="text-xl font-bold text-emerald-400">0</p>
                </div>
                <div className="bg-[#1e293b] p-4 rounded-xl border border-slate-800">
                    <p className="text-slate-500 text-xs font-bold uppercase mb-1">Overdue</p>
                    <p className="text-xl font-bold text-red-400">0</p>
                </div>
            </div>

            <div className="bg-[#1e293b] border border-slate-800 rounded-2xl overflow-hidden shadow-2xl">
                <div className="p-4 border-b border-slate-800 flex items-center justify-between bg-slate-900/20">
                    <div className="relative w-96">
                        <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" />
                        <input
                            type="text"
                            placeholder="Search projects..."
                            className="w-full bg-slate-900 border border-slate-700 rounded-lg py-2 pl-10 pr-4 text-sm text-white focus:ring-1 focus:ring-blue-500 outline-none transition-all"
                        />
                    </div>
                </div>

                <div className="overflow-x-auto">
                    <table className="w-full text-left">
                        <thead>
                            <tr className="bg-slate-900/50 text-slate-500 text-[10px] font-bold uppercase tracking-widest">
                                <th className="px-6 py-4">Project Code</th>
                                <th className="px-6 py-4">Project Name</th>
                                <th className="px-6 py-4">Client</th>
                                <th className="px-6 py-4">Status</th>
                                <th className="px-6 py-4">Due Date</th>
                                <th className="px-6 py-4"></th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-slate-800/50">
                            {loading ? (
                                [1, 2, 3].map(i => <tr key={i} className="animate-pulse h-16 bg-slate-800/10"></tr>)
                            ) : projects.length === 0 ? (
                                <tr>
                                    <td colSpan={6} className="px-6 py-20 text-center text-slate-500">
                                        <Briefcase className="w-12 h-12 mx-auto mb-4 opacity-10" />
                                        <p>No projects found. Create your first project to get started.</p>
                                    </td>
                                </tr>
                            ) : null}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
}
