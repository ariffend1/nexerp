'use client';

import { useState, useEffect } from 'react';
import api from '@/lib/api';
import { Users, Plus, Search, Briefcase, Mail } from 'lucide-react';

export default function EmployeesPage() {
    const [employees, setEmployees] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchEmployees = async () => {
            try {
                const response = await api.get('/hr/employees');
                setEmployees(response.data);
            } catch (error) {
                console.error('Error fetching employees:', error);
            } finally {
                setLoading(false);
            }
        };
        fetchEmployees();
    }, []);

    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <div>
                    <h2 className="text-2xl font-bold text-white">Employee Management</h2>
                    <p className="text-slate-400 text-sm">Manage workforce and departments</p>
                </div>
                <button className="bg-purple-600 hover:bg-purple-500 text-white px-4 py-2 rounded-lg flex items-center gap-2 transition-all shadow-lg shadow-purple-500/20">
                    <Plus className="w-4 h-4" />
                    Add Employee
                </button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="bg-[#1e293b] p-6 rounded-2xl border border-slate-800">
                    <h3 className="text-slate-500 text-xs font-bold uppercase mb-4 tracking-wider">Active Employees</h3>
                    <div className="flex items-center gap-4">
                        <div className="p-3 bg-purple-500/10 text-purple-500 rounded-xl">
                            <Users className="w-6 h-6" />
                        </div>
                        <div>
                            <p className="text-2xl font-bold text-white">{employees.length}</p>
                            <p className="text-xs text-slate-500">Across all departments</p>
                        </div>
                    </div>
                </div>
                <div className="bg-[#1e293b] p-6 rounded-2xl border border-slate-800">
                    <h3 className="text-slate-500 text-xs font-bold uppercase mb-4 tracking-wider">Departments</h3>
                    <div className="flex items-center gap-4">
                        <div className="p-3 bg-cyan-500/10 text-cyan-500 rounded-xl">
                            <Briefcase className="w-6 h-6" />
                        </div>
                        <div>
                            <p className="text-2xl font-bold text-white">8</p>
                            <p className="text-xs text-slate-500">Operational units</p>
                        </div>
                    </div>
                </div>
                <div className="bg-[#1e293b] p-6 rounded-2xl border border-slate-800">
                    <h3 className="text-slate-500 text-xs font-bold uppercase mb-4 tracking-wider">Payroll Budget</h3>
                    <div className="flex items-center gap-4">
                        <div className="p-3 bg-emerald-500/10 text-emerald-500 rounded-xl">
                            <Mail className="w-6 h-6" />
                        </div>
                        <div>
                            <p className="text-2xl font-bold text-white">$124k</p>
                            <p className="text-xs text-slate-500">Monthly total</p>
                        </div>
                    </div>
                </div>
            </div>

            <div className="bg-[#1e293b] border border-slate-800 rounded-2xl overflow-hidden shadow-2xl">
                <div className="p-4 border-b border-slate-800 flex items-center justify-between bg-slate-900/20">
                    <div className="relative w-96">
                        <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" />
                        <input
                            type="text"
                            placeholder="Search employees..."
                            className="w-full bg-slate-900 border border-slate-700 rounded-lg py-2 pl-10 pr-4 text-sm text-white focus:ring-1 focus:ring-purple-500 outline-none transition-all"
                        />
                    </div>
                </div>

                <div className="overflow-x-auto">
                    <table className="w-full text-left border-collapse">
                        <thead>
                            <tr className="bg-slate-900/50 text-slate-500 text-[10px] font-bold uppercase tracking-widest">
                                <th className="px-6 py-4">Employee ID</th>
                                <th className="px-6 py-4">Full Name</th>
                                <th className="px-6 py-4">Job Title</th>
                                <th className="px-6 py-4">Contact</th>
                                <th className="px-6 py-4 text-right">Salary</th>
                                <th className="px-6 py-4"></th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-slate-800/50">
                            {loading ? (
                                [1, 2, 3].map(i => <tr key={i} className="animate-pulse h-16 bg-slate-800/10"></tr>)
                            ) : employees.length === 0 ? (
                                <tr>
                                    <td colSpan={6} className="px-6 py-20 text-center text-slate-500">
                                        <Users className="w-12 h-12 mx-auto mb-4 opacity-10" />
                                        <p>No employees found. Add your first team member.</p>
                                    </td>
                                </tr>
                            ) : employees.map((emp: any) => (
                                <tr key={emp.id} className="hover:bg-slate-800/20 transition-colors">
                                    <td className="px-6 py-4 font-mono text-xs font-bold text-purple-400">
                                        {emp.employee_code}
                                    </td>
                                    <td className="px-6 py-4">
                                        <p className="text-sm font-medium text-white">{emp.full_name}</p>
                                    </td>
                                    <td className="px-6 py-4 text-xs text-slate-400">{emp.job_title}</td>
                                    <td className="px-6 py-4">
                                        <div className="flex flex-col gap-1">
                                            <span className="text-xs text-slate-400 flex items-center gap-1">
                                                <Mail className="w-3 h-3" /> {emp.email}
                                            </span>
                                        </div>
                                    </td>
                                    <td className="px-6 py-4 text-right text-sm font-bold text-white">
                                        ${emp.base_salary?.toLocaleString() || '0'}
                                    </td>
                                    <td className="px-6 py-4 text-right text-slate-500">
                                        <button className="hover:text-white transition-colors">Details</button>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
}
