'use client';

import { useState, useEffect } from 'react';
import api from '@/lib/api';
import { Package, Plus, Search, Filter, MoreVertical } from 'lucide-react';

export default function InventoryPage() {
    const [products, setProducts] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchProducts = async () => {
            try {
                const response = await api.get('/products');
                setProducts(response.data);
            } catch (error) {
                console.error('Error fetching products:', error);
            } finally {
                setLoading(false);
            }
        };
        fetchProducts();
    }, []);

    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <div>
                    <h2 className="text-2xl font-bold text-white">Inventory Management</h2>
                    <p className="text-slate-400 text-sm">Track and manage your stock levels</p>
                </div>
                <button className="bg-blue-600 hover:bg-blue-500 text-white px-4 py-2 rounded-lg flex items-center gap-2 transition-all">
                    <Plus className="w-4 h-4" />
                    Add Item
                </button>
            </div>

            <div className="bg-[#1e293b] border border-slate-800 rounded-2xl overflow-hidden">
                {/* Table Filters */}
                <div className="p-4 border-b border-slate-800 flex flex-wrap gap-4 items-center justify-between">
                    <div className="relative w-80">
                        <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" />
                        <input
                            type="text"
                            placeholder="Search items..."
                            className="w-full bg-slate-900 border border-slate-700 rounded-lg py-1.5 pl-10 pr-4 text-sm text-white focus:ring-1 focus:ring-blue-500 outline-none"
                        />
                    </div>
                    <div className="flex gap-2">
                        <button className="bg-slate-900 border border-slate-700 text-slate-300 px-3 py-1.5 rounded-lg text-sm flex items-center gap-2 hover:bg-slate-800">
                            <Filter className="w-4 h-4" />
                            Filter
                        </button>
                    </div>
                </div>

                {/* Inventory Table */}
                <div className="overflow-x-auto">
                    <table className="w-full text-left border-collapse">
                        <thead>
                            <tr className="bg-slate-900/50 text-slate-400 text-xs uppercase tracking-wider">
                                <th className="px-6 py-4 font-semibold">Product</th>
                                <th className="px-6 py-4 font-semibold">SKU / Code</th>
                                <th className="px-6 py-4 font-semibold">Type</th>
                                <th className="px-6 py-4 font-semibold text-right">Stock</th>
                                <th className="px-6 py-4 font-semibold">UOM</th>
                                <th className="px-6 py-4 font-semibold text-right">Value</th>
                                <th className="px-6 py-4"></th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-slate-800">
                            {loading ? (
                                [1, 2, 3].map(i => (
                                    <tr key={i} className="animate-pulse">
                                        <td colSpan={7} className="px-6 py-4 bg-slate-800/20 h-12"></td>
                                    </tr>
                                ))
                            ) : products.length === 0 ? (
                                <tr>
                                    <td colSpan={7} className="px-6 py-20 text-center text-slate-500">
                                        <Package className="w-12 h-12 mx-auto mb-4 opacity-20" />
                                        <p>No inventory items found. Add your first product to get started.</p>
                                    </td>
                                </tr>
                            ) : products.map((product: any) => (
                                <tr key={product.id} className="hover:bg-slate-800/30 transition-colors group">
                                    <td className="px-6 py-4">
                                        <span className="text-sm font-medium text-white">{product.name}</span>
                                    </td>
                                    <td className="px-6 py-4">
                                        <span className="text-xs text-slate-400 font-mono">{product.code}</span>
                                    </td>
                                    <td className="px-6 py-4">
                                        <span className="px-2 py-0.5 rounded text-[10px] font-bold uppercase bg-slate-900 text-slate-400 border border-slate-700">
                                            {product.type}
                                        </span>
                                    </td>
                                    <td className="px-6 py-4 text-right">
                                        <span className="text-sm font-bold text-white">0</span>
                                    </td>
                                    <td className="px-6 py-4">
                                        <span className="text-xs text-slate-500 uppercase">{product.uom}</span>
                                    </td>
                                    <td className="px-6 py-4 text-right">
                                        <span className="text-sm text-slate-300">$0.00</span>
                                    </td>
                                    <td className="px-6 py-4 text-right">
                                        <button className="text-slate-500 hover:text-white transition-colors">
                                            <MoreVertical className="w-4 h-4" />
                                        </button>
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
