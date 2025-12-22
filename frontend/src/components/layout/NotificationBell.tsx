'use client';

import { useState, useEffect } from 'react';
import api from '@/lib/api';
import { Bell, Check, X, Clock } from 'lucide-react';

export default function NotificationBell() {
    const [notifications, setNotifications] = useState([]);
    const [unreadCount, setUnreadCount] = useState(0);
    const [isOpen, setIsOpen] = useState(false);

    const fetchNotifications = async () => {
        try {
            const response = await api.get('/notifications');
            setNotifications(response.data);
        } catch (error) {
            console.error('Error fetching notifications:', error);
        }
    };

    const fetchUnreadCount = async () => {
        try {
            const response = await api.get('/notifications/unread-count');
            setUnreadCount(response.data.unread_count);
        } catch (error) {
            console.error('Error fetching unread count:', error);
        }
    };

    const markAsRead = async (id: string) => {
        try {
            await api.post(`/notifications/${id}/mark-read`);
            fetchNotifications();
            fetchUnreadCount();
        } catch (error) {
            console.error('Error marking as read:', error);
        }
    };

    useEffect(() => {
        fetchNotifications();
        fetchUnreadCount();
        // Poll for new notifications every 30 seconds
        const interval = setInterval(() => {
            fetchUnreadCount();
        }, 30000);
        return () => clearInterval(interval);
    }, []);

    const getPriorityColor = (priority: string) => {
        switch (priority) {
            case 'urgent': return 'text-red-400 bg-red-500/10';
            case 'high': return 'text-orange-400 bg-orange-500/10';
            case 'medium': return 'text-blue-400 bg-blue-500/10';
            default: return 'text-slate-400 bg-slate-500/10';
        }
    };

    const getIcon = (type: string) => {
        if (type.includes('approval')) return Clock;
        return Bell;
    };

    return (
        <div className="relative">
            <button
                onClick={() => setIsOpen(!isOpen)}
                className="relative text-slate-400 hover:text-white transition-colors"
            >
                <Bell className="w-5 h-5" />
                {unreadCount > 0 && (
                    <span className="absolute -top-1 -right-1 bg-red-500 text-white text-[10px] font-bold rounded-full w-4 h-4 flex items-center justify-center">
                        {unreadCount > 9 ? '9+' : unreadCount}
                    </span>
                )}
            </button>

            {isOpen && (
                <div className="absolute right-0 mt-2 w-96 bg-[#1e293b] border border-slate-700 rounded-xl shadow-2xl z-50 max-h-[500px] overflow-hidden">
                    <div className="p-4 border-b border-slate-700 flex justify-between items-center">
                        <h3 className="font-semibold text-white">Notifications</h3>
                        <button onClick={() => setIsOpen(false)} className="text-slate-500 hover:text-white">
                            <X className="w-4 h-4" />
                        </button>
                    </div>

                    <div className="overflow-y-auto max-h-96">
                        {notifications.length === 0 ? (
                            <div className="p-8 text-center text-slate-500">
                                <Bell className="w-12 h-12 mx-auto mb-2 opacity-20" />
                                <p className="text-sm">No notifications yet</p>
                            </div>
                        ) : (
                            notifications.map((notif: any) => {
                                const Icon = getIcon(notif.type);
                                return (
                                    <div
                                        key={notif.id}
                                        className={`p-4 border-b border-slate-800 hover:bg-slate-800/30 transition-colors ${notif.is_read ? 'opacity-60' : ''
                                            }`}
                                    >
                                        <div className="flex items-start gap-3">
                                            <div className={`p-2 rounded-lg ${getPriorityColor(notif.priority)}`}>
                                                <Icon className="w-4 h-4" />
                                            </div>
                                            <div className="flex-1 min-w-0">
                                                <h4 className="text-sm font-medium text-white truncate">{notif.title}</h4>
                                                <p className="text-xs text-slate-400 mt-1">{notif.message}</p>
                                                <p className="text-[10px] text-slate-600 mt-1">{new Date(notif.created_at).toLocaleString()}</p>
                                            </div>
                                            {!notif.is_read && (
                                                <button
                                                    onClick={() => markAsRead(notif.id)}
                                                    className="text-blue-400 hover:text-blue-300"
                                                >
                                                    <Check className="w-4 h-4" />
                                                </button>
                                            )}
                                        </div>
                                    </div>
                                );
                            })
                        )}
                    </div>
                </div>
            )}
        </div>
    );
}
