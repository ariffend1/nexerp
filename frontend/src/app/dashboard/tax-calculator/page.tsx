'use client';

import { useState } from 'react';
import { Calculator, DollarSign, FileText, TrendingUp } from 'lucide-react';
import api from '@/lib/api';

export default function TaxCalculatorPage() {
    const [activeTab, setActiveTab] = useState('ppn');
    const [results, setResults] = useState<any>(null);
    const [loading, setLoading] = useState(false);

    // PPN Calculator
    const [ppnAmount, setPpnAmount] = useState('');
    const [includeTax, setIncludeTax] = useState(false);

    // PPh 21 Calculator
    const [annualIncome, setAnnualIncome] = useState('');
    const [hasNPWP21, setHasNPWP21] = useState(true);

    // PPh 23 Calculator
    const [pph23Amount, setPph23Amount] = useState('');
    const [hasNPWP23, setHasNPWP23] = useState(true);

    // PPh 4(2) Calculator
    const [pph42Amount, setPph42Amount] = useState('');
    const [serviceType, setServiceType] = useState('construction');

    const calculatePPN = async () => {
        setLoading(true);
        try {
            const response = await api.post('/currency-tax/tax/ppn/calculate', {
                amount: parseFloat(ppnAmount),
                include_tax: includeTax
            });
            setResults(response.data);
        } catch (error) {
            console.error('Error calculating PPN:', error);
        } finally {
            setLoading(false);
        }
    };

    const calculatePPh21 = async () => {
        setLoading(true);
        try {
            const response = await api.post('/currency-tax/tax/pph21/calculate', {
                annual_income: parseFloat(annualIncome),
                has_npwp: hasNPWP21
            });
            setResults(response.data);
        } catch (error) {
            console.error('Error calculating PPh 21:', error);
        } finally {
            setLoading(false);
        }
    };

    const calculatePPh23 = async () => {
        setLoading(true);
        try {
            const response = await api.post('/currency-tax/tax/pph23/calculate', {
                amount: parseFloat(pph23Amount),
                has_npwp: hasNPWP23
            });
            setResults(response.data);
        } catch (error) {
            console.error('Error calculating PPh 23:', error);
        } finally {
            setLoading(false);
        }
    };

    const calculatePPh42 = async () => {
        setLoading(true);
        try {
            const response = await api.post('/currency-tax/tax/pph42/calculate', {
                amount: parseFloat(pph42Amount),
                service_type: serviceType
            });
            setResults(response.data);
        } catch (error) {
            console.error('Error calculating PPh 4(2):', error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="space-y-6">
            <div>
                <h1 className="text-3xl font-bold text-white mb-2">Indonesian Tax Calculator</h1>
                <p className="text-slate-400">Calculate PPN, PPh 21, PPh 23, and PPh 4(2) with ease</p>
            </div>

            {/* Tabs */}
            <div className="flex gap-2 border-b border-slate-800">
                {[
                    { id: 'ppn', label: 'PPN (VAT)', icon: Calculator },
                    { id: 'pph21', label: 'PPh 21', icon: TrendingUp },
                    { id: 'pph23', label: 'PPh 23', icon: DollarSign },
                    { id: 'pph42', label: 'PPh 4(2)', icon: FileText }
                ].map((tab) => (
                    <button
                        key={tab.id}
                        onClick={() => { setActiveTab(tab.id); setResults(null); }}
                        className={`flex items-center gap-2 px-4 py-3 font-medium transition-all ${activeTab === tab.id
                                ? 'text-blue-400 border-b-2 border-blue-400'
                                : 'text-slate-400 hover:text-white'
                            }`}
                    >
                        <tab.icon className="w-4 h-4" />
                        {tab.label}
                    </button>
                ))}
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Input Form */}
                <div className="bg-[#1e293b] border border-slate-800 rounded-2xl p-6">
                    <h3 className="text-white font-semibold mb-4">Calculator Input</h3>

                    {activeTab === 'ppn' && (
                        <div className="space-y-4">
                            <div>
                                <label className="block text-sm font-medium text-slate-300 mb-2">Amount (IDR)</label>
                                <input
                                    type="number"
                                    value={ppnAmount}
                                    onChange={(e) => setPpnAmount(e.target.value)}
                                    className="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-3 text-white focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
                                    placeholder="10000000"
                                />
                            </div>
                            <div className="flex items-center gap-2">
                                <input
                                    type="checkbox"
                                    checked={includeTax}
                                    onChange={(e) => setIncludeTax(e.target.checked)}
                                    className="w-4 h-4 text-blue-600 bg-slate-900 border-slate-700 rounded focus:ring-blue-500"
                                />
                                <label className="text-sm text-slate-300">Amount includes PPN</label>
                            </div>
                            <button
                                onClick={calculatePPN}
                                disabled={!ppnAmount || loading}
                                className="w-full bg-blue-600 hover:bg-blue-500 disabled:bg-slate-700 text-white py-3 rounded-lg font-medium transition-all"
                            >
                                {loading ? 'Calculating...' : 'Calculate PPN'}
                            </button>
                            <div className="mt-4 p-4 bg-blue-900/20 border border-blue-500/30 rounded-lg">
                                <p className="text-xs text-blue-400">ℹ️ PPN (Pajak Pertambahan Nilai) = VAT 11%</p>
                            </div>
                        </div>
                    )}

                    {activeTab === 'pph21' && (
                        <div className="space-y-4">
                            <div>
                                <label className="block text-sm font-medium text-slate-300 mb-2">Annual Income (IDR)</label>
                                <input
                                    type="number"
                                    value={annualIncome}
                                    onChange={(e) => setAnnualIncome(e.target.value)}
                                    className="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-3 text-white focus:border-purple-500 focus:ring-1 focus:ring-purple-500"
                                    placeholder="100000000"
                                />
                            </div>
                            <div className="flex items-center gap-2">
                                <input
                                    type="checkbox"
                                    checked={hasNPWP21}
                                    onChange={(e) => setHasNPWP21(e.target.checked)}
                                    className="w-4 h-4 text-purple-600 bg-slate-900 border-slate-700 rounded focus:ring-purple-500"
                                />
                                <label className="text-sm text-slate-300">Has NPWP (Tax ID)</label>
                            </div>
                            <button
                                onClick={calculatePPh21}
                                disabled={!annualIncome || loading}
                                className="w-full bg-purple-600 hover:bg-purple-500 disabled:bg-slate-700 text-white py-3 rounded-lg font-medium transition-all"
                            >
                                {loading ? 'Calculating...' : 'Calculate PPh 21'}
                            </button>
                            <div className="mt-4 p-4 bg-purple-900/20 border border-purple-500/30 rounded-lg">
                                <p className="text-xs text-purple-400">ℹ️ PPh 21 = Income Tax (Progressive 5%-35%)</p>
                                <p className="text-xs text-purple-400 mt-1">PTKP: Rp 54,000,000 (single, no dependents)</p>
                            </div>
                        </div>
                    )}

                    {activeTab === 'pph23' && (
                        <div className="space-y-4">
                            <div>
                                <label className="block text-sm font-medium text-slate-300 mb-2">Gross Amount (IDR)</label>
                                <input
                                    type="number"
                                    value={pph23Amount}
                                    onChange={(e) => setPph23Amount(e.target.value)}
                                    className="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-3 text-white focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500"
                                    placeholder="5000000"
                                />
                            </div>
                            <div className="flex items-center gap-2">
                                <input
                                    type="checkbox"
                                    checked={hasNPWP23}
                                    onChange={(e) => setHasNPWP23(e.target.checked)}
                                    className="w-4 h-4 text-emerald-600 bg-slate-900 border-slate-700 rounded focus:ring-emerald-500"
                                />
                                <label className="text-sm text-slate-300">Has NPWP (2%, else 4%)</label>
                            </div>
                            <button
                                onClick={calculatePPh23}
                                disabled={!pph23Amount || loading}
                                className="w-full bg-emerald-600 hover:bg-emerald-500 disabled:bg-slate-700 text-white py-3 rounded-lg font-medium transition-all"
                            >
                                {loading ? 'Calculating...' : 'Calculate PPh 23'}
                            </button>
                            <div className="mt-4 p-4 bg-emerald-900/20 border border-emerald-500/30 rounded-lg">
                                <p className="text-xs text-emerald-400">ℹ️ PPh 23 = Withholding Tax for services/rent</p>
                            </div>
                        </div>
                    )}

                    {activeTab === 'pph42' && (
                        <div className="space-y-4">
                            <div>
                                <label className="block text-sm font-medium text-slate-300 mb-2">Gross Amount (IDR)</label>
                                <input
                                    type="number"
                                    value={pph42Amount}
                                    onChange={(e) => setPph42Amount(e.target.value)}
                                    className="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-3 text-white focus:border-amber-500 focus:ring-1 focus:ring-amber-500"
                                    placeholder="10000000"
                                />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-slate-300 mb-2">Service Type</label>
                                <select
                                    value={serviceType}
                                    onChange={(e) => setServiceType(e.target.value)}
                                    className="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-3 text-white focus:border-amber-500 focus:ring-1 focus:ring-amber-500"
                                >
                                    <option value="construction">Construction (2.5%)</option>
                                    <option value="rent">Rent (10%)</option>
                                    <option value="other">Other Services (10%)</option>
                                </select>
                            </div>
                            <button
                                onClick={calculatePPh42}
                                disabled={!pph42Amount || loading}
                                className="w-full bg-amber-600 hover:bg-amber-500 disabled:bg-slate-700 text-white py-3 rounded-lg font-medium transition-all"
                            >
                                {loading ? 'Calculating...' : 'Calculate PPh 4(2)'}
                            </button>
                            <div className="mt-4 p-4 bg-amber-900/20 border border-amber-500/30 rounded-lg">
                                <p className="text-xs text-amber-400">ℹ️ PPh 4(2) = Final Tax (non-refundable)</p>
                            </div>
                        </div>
                    )}
                </div>

                {/* Results */}
                <div className="bg-[#1e293b] border border-slate-800 rounded-2xl p-6">
                    <h3 className="text-white font-semibold mb-4">Calculation Results</h3>

                    {!results ? (
                        <div className="flex flex-col items-center justify-center h-64 text-slate-500">
                            <Calculator className="w-16 h-16 mb-4" />
                            <p>Enter values and calculate to see results</p>
                        </div>
                    ) : (
                        <div className="space-y-4">
                            {activeTab === 'ppn' && results && (
                                <>
                                    <div className="flex justify-between p-3 bg-slate-900/50 rounded-lg">
                                        <span className="text-slate-400">Base Amount</span>
                                        <span className="text-white font-bold">Rp {results.base_amount?.toLocaleString()}</span>
                                    </div>
                                    <div className="flex justify-between p-3 bg-blue-900/20 border border-blue-500/30 rounded-lg">
                                        <span className="text-blue-400 font-medium">PPN ({results.ppn_rate}%)</span>
                                        <span className="text-blue-400 font-bold">Rp {results.ppn_amount?.toLocaleString()}</span>
                                    </div>
                                    <div className="flex justify-between p-4 bg-gradient-to-r from-emerald-900/30 to-emerald-800/20 rounded-lg border-l-4 border-emerald-400">
                                        <span className="text-white font-semibold">Total Amount</span>
                                        <span className="text-2xl text-emerald-400 font-bold">Rp {results.total_amount?.toLocaleString()}</span>
                                    </div>
                                </>
                            )}

                            {activeTab === 'pph21' && results && (
                                <>
                                    <div className="flex justify-between p-3 bg-slate-900/50 rounded-lg">
                                        <span className="text-slate-400">Annual Income</span>
                                        <span className="text-white font-bold">Rp {results.annual_income?.toLocaleString()}</span>
                                    </div>
                                    <div className="flex justify-between p-3 bg-slate-900/50 rounded-lg">
                                        <span className="text-slate-400">PTKP (Tax-free)</span>
                                        <span className="text-white font-bold">Rp {results.ptkp?.toLocaleString()}</span>
                                    </div>
                                    <div className="flex justify-between p-3 bg-slate-900/50 rounded-lg">
                                        <span className="text-slate-400">Taxable Income</span>
                                        <span className="text-white font-bold">Rp {results.taxable_income?.toLocaleString()}</span>
                                    </div>
                                    <div className="flex justify-between p-4 bg-gradient-to-r from-purple-900/30 to-purple-800/20 rounded-lg border-l-4 border-purple-400">
                                        <span className="text-white font-semibold">PPh 21 Tax</span>
                                        <span className="text-2xl text-purple-400 font-bold">Rp {results.tax_amount?.toLocaleString()}</span>
                                    </div>
                                    <div className="flex justify-between p-3 bg-slate-900/50 rounded-lg">
                                        <span className="text-slate-400">Effective Rate</span>
                                        <span className="text-white font-bold">{results.effective_rate?.toFixed(2)}%</span>
                                    </div>
                                </>
                            )}

                            {activeTab === 'pph23' && results && (
                                <>
                                    <div className="flex justify-between p-3 bg-slate-900/50 rounded-lg">
                                        <span className="text-slate-400">Gross Amount</span>
                                        <span className="text-white font-bold">Rp {results.gross_amount?.toLocaleString()}</span>
                                    </div>
                                    <div className="flex justify-between p-3 bg-emerald-900/20 border border-emerald-500/30 rounded-lg">
                                        <span className="text-emerald-400">PPh 23 ({results.tax_rate}%)</span>
                                        <span className="text-emerald-400 font-bold">Rp {results.tax_amount?.toLocaleString()}</span>
                                    </div>
                                    <div className="flex justify-between p-4 bg-gradient-to-r from-blue-900/30 to-blue-800/20 rounded-lg border-l-4 border-blue-400">
                                        <span className="text-white font-semibold">Net Amount</span>
                                        <span className="text-2xl text-blue-400 font-bold">Rp {results.net_amount?.toLocaleString()}</span>
                                    </div>
                                </>
                            )}

                            {activeTab === 'pph42' && results && (
                                <>
                                    <div className="flex justify-between p-3 bg-slate-900/50 rounded-lg">
                                        <span className="text-slate-400">Gross Amount</span>
                                        <span className="text-white font-bold">Rp {results.gross_amount?.toLocaleString()}</span>
                                    </div>
                                    <div className="flex justify-between p-3 bg-slate-900/50 rounded-lg">
                                        <span className="text-slate-400">Service Type</span>
                                        <span className="text-white font-bold capitalize">{results.service_type}</span>
                                    </div>
                                    <div className="flex justify-between p-3 bg-amber-900/20 border border-amber-500/30 rounded-lg">
                                        <span className="text-amber-400">PPh 4(2) ({results.tax_rate}%)</span>
                                        <span className="text-amber-400 font-bold">Rp {results.tax_amount?.toLocaleString()}</span>
                                    </div>
                                    <div className="flex justify-between p-4 bg-gradient-to-r from-emerald-900/30 to-emerald-800/20 rounded-lg border-l-4 border-emerald-400">
                                        <span className="text-white font-semibold">Net Amount</span>
                                        <span className="text-2xl text-emerald-400 font-bold">Rp {results.net_amount?.toLocaleString()}</span>
                                    </div>
                                </>
                            )}
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
