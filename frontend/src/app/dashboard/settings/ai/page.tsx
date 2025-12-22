'use client';

import { useState, useEffect } from 'react';
import api from '@/lib/api';
import { Brain, Zap, AlertTriangle, TrendingUp, MessageSquare, Tag, Save, Info } from 'lucide-react';

export default function AISettingsPage() {
    const [settings, setSettings] = useState<any>(null);
    const [loading, setLoading] = useState(true);
    const [saving, setSaving] = useState(false);

    useEffect(() => {
        fetchSettings();
    }, []);

    const fetchSettings = async () => {
        try {
            const response = await api.get('/ai/settings');
            setSettings(response.data);
        } catch (error) {
            console.error('Error fetching AI settings:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleToggle = (field: string) => {
        setSettings((prev: any) => ({
            ...prev,
            [field]: !prev[field]
        }));
    };

    const saveSettings = async () => {
        setSaving(true);
        try {
            await api.put('/ai/settings', settings);
            alert('AI settings saved successfully!');
        } catch (error) {
            console.error('Error saving settings:', error);
            alert('Failed toсохранить settings');
        } finally {
            setSaving(false);
        }
    };

    if (loading) {
        return (
            <div className="flex items-center justify-center min-h-screen">
                <div className="text-center">
                    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-500 mx-auto mb-4"></div>
                    <p className="text-slate-400">Loading AI settings...</p>
                </div>
            </div>
        );
    }

    const features = [
        {
            id: 'anomaly_detection_enabled',
            icon: AlertTriangle,
            title: 'Anomaly Detection',
            description: 'Automatically detect unusual patterns in transactions, sales, and expenses',
            color: 'red',
            resourceImpact: 'Low'
        },
        {
            id: 'predictive_analytics_enabled',
            icon: TrendingUp,
            title: 'Predictive Analytics',
            description: 'Forecast sales, demand, and cash flow using ML models',
            color: 'purple',
            resourceImpact: 'Medium'
        },
        {
            id: 'smart_recommendations_enabled',
            icon: Zap,
            title: 'Smart Recommendations',
            description: 'Get AI-powered business insights and actionable suggestions',
            color: 'blue',
            resourceImpact: 'Low'
        },
        {
            id: 'natural_language_query_enabled',
            icon: MessageSquare,
            title: 'Natural Language Queries',
            description: 'Ask questions in plain language: "Show me top 10 customers this month"',
            color: 'emerald',
            resourceImpact: 'High'
        },
        {
            id: 'auto_categorization_enabled',
            icon: Tag,
            title: 'Auto-Categorization',
            description: 'Automatically categorize expenses, revenues, and documents',
            color: 'amber',
            resourceImpact: 'Low'
        }
    ];

    const totalEnabled = features.filter(f => settings?.[f.id]).length;

    return (
        <div className="space-y-6">
            {/* Header */}
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-3xl font-bold text-white mb-2 flex items-center gap-3">
                        <Brain className="w-8 h-8 text-purple-400" />
                        AI Features Control
                    </h1>
                    <p className="text-slate-400">Manage AI capabilities and resource usage</p>
                </div>
                <button
                    onClick={saveSettings}
                    disabled={saving}
                    className="bg-purple-600 hover:bg-purple-500 disabled:bg-slate-700 text-white px-6 py-3 rounded-lg font-medium transition-all flex items-center gap-2"
                >
                    <Save className="w-4 h-4" />
                    {saving ? 'Saving...' : 'Save Settings'}
                </button>
            </div>

            {/* Summary Card */}
            <div className="bg-gradient-to-r from-purple-900/30 to-purple-800/20 border border-purple-500/30 rounded-2xl p-6">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <div className="text-center">
                        <p className="text-purple-400 text-sm font-medium mb-1">Active Features</p>
                        <p className="text-4xl font-bold text-white">{totalEnabled}/{features.length}</p>
                    </div>
                    <div className="text-center">
                        <p className="text-purple-400 text-sm font-medium mb-1">Daily AI Calls Limit</p>
                        <p className="text-4xl font-bold text-white">{settings?.max_ai_calls_per_day || 100}</p>
                    </div>
                    <div className="text-center">
                        <p className="text-purple-400 text-sm font-medium mb-1">Resource Impact</p>
                        <p className="text-4xl font-bold text-white">
                            {totalEnabled === 0 ? 'None' : totalEnabled <= 2 ? 'Low' : totalEnabled <= 4 ? 'Medium' : 'High'}
                        </p>
                    </div>
                </div>
            </div>

            {/* Warning Notice */}
            <div className="bg-amber-900/20 border border-amber-500/30 rounded-xl p-4 flex items-start gap-3">
                <Info className="w-5 h-5 text-amber-400 flex-shrink-0 mt-0.5" />
                <div className="flex-1">
                    <p className="text-amber-400 font-medium mb-1">Resource Management</p>
                    <p className="text-sm text-slate-300">
                        AI features consume server resources. Enable only what you need. Features marked &quot;High&quot; impact
                        may slow down system on limited servers. You can always toggle them on/off.
                    </p>
                </div>
            </div>

            {/* Feature Toggles */}
            <div className="space-y-4">
                {features.map((feature) => (
                    <div
                        key={feature.id}
                        className={`bg-[#1e293b] border ${settings?.[feature.id]
                                ? `border-${feature.color}-500/50 bg-gradient-to-r from-${feature.color}-900/10 to-transparent`
                                : 'border-slate-800'
                            } rounded-2xl p-6 transition-all`}
                    >
                        <div className="flex items-start justify-between">
                            <div className="flex items-start gap-4 flex-1">
                                <div className={`p-3 rounded-xl bg-${feature.color}-500/10 border border-${feature.color}-500/20`}>
                                    <feature.icon className={`w-6 h-6 text-${feature.color}-400`} />
                                </div>
                                <div className="flex-1">
                                    <div className="flex items-center gap-3 mb-2">
                                        <h3 className="text-white font-semibold text-lg">{feature.title}</h3>
                                        <span className={`px-2 py-0.5 rounded-full text-xs font-bold ${feature.resourceImpact === 'Low' ? 'bg-emerald-500/20 text-emerald-400' :
                                                feature.resourceImpact === 'Medium' ? 'bg-amber-500/20 text-amber-400' :
                                                    'bg-red-500/20 text-red-400'
                                            }`}>
                                            {feature.resourceImpact} Impact
                                        </span>
                                    </div>
                                    <p className="text-slate-400 text-sm">{feature.description}</p>
                                </div>
                            </div>

                            {/* Toggle Switch */}
                            <button
                                onClick={() => handleToggle(feature.id)}
                                className={`relative inline-flex h-8 w-14 items-center rounded-full transition-colors ${settings?.[feature.id] ? `bg-${feature.color}-600` : 'bg-slate-700'
                                    }`}
                            >
                                <span
                                    className={`inline-block h-6 w-6 transform rounded-full bg-white transition-transform ${settings?.[feature.id] ? 'translate-x-7' : 'translate-x-1'
                                        }`}
                                />
                            </button>
                        </div>
                    </div>
                ))}
            </div>

            {/* Advanced Settings */}
            <div className="bg-[#1e293b] border border-slate-800 rounded-2xl p-6">
                <h3 className="text-white font-semibold mb-4">Advanced Configuration</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                        <label className="block text-sm font-medium text-slate-300 mb-2">
                            AI Model Preference
                        </label>
                        <select
                            value={settings?.ai_model_preference || 'standard'}
                            onChange={(e) => setSettings((prev: any) => ({ ...prev, ai_model_preference: e.target.value }))}
                            className="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-3 text-white focus:border-purple-500 focus:ring-1 focus:ring-purple-500"
                        >
                            <option value="standard">Standard (Fastest, Lower cost)</option>
                            <option value="advanced">Advanced (Better accuracy)</option>
                            <option value="custom">Custom (Your model)</option>
                        </select>
                    </div>
                    <div>
                        <label className="block text-sm font-medium text-slate-300 mb-2">
                            Max AI Calls per Day
                        </label>
                        <input
                            type="number"
                            value={settings?.max_ai_calls_per_day || 100}
                            onChange={(e) => setSettings((prev: any) => ({ ...prev, max_ai_calls_per_day: parseInt(e.target.value) }))}
                            className="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-3 text-white focus:border-purple-500 focus:ring-1 focus:ring-purple-500"
                            min="0"
                            max="10000"
                        />
                    </div>
                </div>
            </div>
        </div>
    );
}
