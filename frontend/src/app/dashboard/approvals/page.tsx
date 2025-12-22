'use client';

import { useState, useEffect } from 'react';
import api from '@/lib/api';
import { CheckCircle, XCircle, Clock, FileText } from 'lucide-react';

export default function ApprovalsPage() {
    const [approvals, setApprovals] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchApprovals();
    }, []);

    const fetchApprovals = async () => {
        try {
            const response = await api.get('/notifications/approvals');
            setApprovals(response.data);
        } catch (error) {
            console.error('Error fetching approvals:', error);
        } finally {
            setLoading(false);
        }
    };

    const approveRequest = async (id: string) => {
        try {
            await api.post(`/notifications/approvals/${id}/approve`, { comments: 'Approved via dashboard' });
            fetchApprovals();
        } catch (error) {
            console.error('Error approving:', error);
        }
    };

    const rejectRequest = async (id: string) => {
        const reason = prompt('Please provide a reason for rejection:');
        if (!reason) return;

        try {
            await api.post(`/notifications/approvals/${id}/reject`, { comments: reason });
            fetchApprovals();
        } catch (error) {
            console.error('Error rejecting:', error);
        }
    };

    return (
        <div className="space-y-6">
            <div>
                <h2 className="text-2xl font-bold text-white">Approval Center</h2>
                <p className="text-slate-400 text-sm">Review and approve pending requests</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="bg-[#1e293b] p-6 rounded-2xl border border-slate-800">
                    <h3 className="text-slate-500 text-xs font-bold uppercase mb-4 tracking-wider">Pending Approvals</h3>
                    <div className="flex items-center gap-4">
                        <div className="p-3 bg-amber-500/10 text-amber-500 rounded-xl">
                            <Clock className="w-6 h-6" />
                        </div>
                        <div>
                            <p className="text-2xl font-bold text-white">{approvals.length}</p>
                            <p className="text-xs text-slate-500">Awaiting your action</p>
                        </div>
                    </div>
                </div>
                <div className="bg-[#1e293b] p-6 rounded-2xl border border-slate-800">
                    <h3 className="text-slate-500 text-xs font-bold uppercase mb-4 tracking-wider">Approved Today</h3>
                    <div className="flex items-center gap-4">
                        <div className="p-3 bg-emerald-500/10 text-emerald-500 rounded-xl">
                            <CheckCircle className="w-6 h-6" />
                        </div>
                        <div>
                            <p className="text-2xl font-bold text-white">12</p>
                            <p className="text-xs text-slate-500">Processed</p>
                        </div>
                    </div>
                </div>
                <div className="bg-[#1e293b] p-6 rounded-2xl border border-slate-800">
                    <h3 className="text-slate-500 text-xs font-bold uppercase mb-4 tracking-wider">Rejected</h3>
                    <div className="flex items-center gap-4">
                        <div className="p-3 bg-red-500/10 text-red-500 rounded-xl">
                            <XCircle className="w-6 h-6" />
                        </div>
                        <div>
                            <p className="text-2xl font-bold text-white">3</p>
                            <p className="text-xs text-slate-500">Declined</p>
                        </div>
                    </div>
                </div>
            </div>

            <div className="bg-[#1e293b] border border-slate-800 rounded-2xl overflow-hidden shadow-2xl">
                <div className="p-4 border-b border-slate-800 bg-slate-900/20">
                    <h3 className="text-white font-semibold">Pending Requests</h3>
                </div>

                <div className="divide-y divide-slate-800">
                    {loading ? (
                        [1, 2, 3].map(i => <div key={i} className="p-6 animate-pulse bg-slate-800/10 h-20"></div>)
                    ) : approvals.length === 0 ? (
                        <div className="p-20 text-center text-slate-500">
                            <CheckCircle className="w-12 h-12 mx-auto mb-4 opacity-20" />
                            <p>No pending approvals. Great job!</p>
                        </div>
                    ) : approvals.map((approval: any) => (
                        <div key={approval.id} className="p-6 hover:bg-slate-800/20 transition-colors">
                            <div className="flex items-center justify-between">
                                <div className="flex items-center gap-4">
                                    <div className="p-3 bg-blue-500/10 text-blue-400 rounded-xl">
                                        <FileText className="w-5 h-5" />
                                    </div>
                                    <div>
                                        <h4 className="text-sm font-medium text-white">{approval.document_type} Approval Request</h4>
                                        <p className="text-xs text-slate-500 mt-1">
                                            Requested on {new Date(approval.requested_at).toLocaleString()}
                                        </p>
                                    </div>
                                </div>
                                <div className="flex gap-2">
                                    <button
                                        onClick={() => approveRequest(approval.id)}
                                        className="bg-emerald-600 hover:bg-emerald-500 text-white px-4 py-2 rounded-lg flex items-center gap-2 text-sm transition-all"
                                    >
                                        <CheckCircle className="w-4 h-4" />
                                        Approve
                                    </button>
                                    <button
                                        onClick={() => rejectRequest(approval.id)}
                                        className="bg-red-600 hover:bg-red-500 text-white px-4 py-2 rounded-lg flex items-center gap-2 text-sm transition-all"
                                    >
                                        <XCircle className="w-4 h-4" />
                                        Reject
                                    </button>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
}
