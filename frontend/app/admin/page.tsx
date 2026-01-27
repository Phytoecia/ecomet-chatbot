"use client";

import { useState, useEffect } from "react";
import clsx from "clsx";

export default function AdminPage() {
    const [password, setPassword] = useState("");
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [logs, setLogs] = useState<any[]>([]);
    const [systemPrompt, setSystemPrompt] = useState("");
    const [status, setStatus] = useState("");
    const [activeTab, setActiveTab] = useState("logs");

    // Use environment variable for backend URL (Systematic Approach)
    const baseUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

    const login = async () => {
        try {
            const res = await fetch(`${baseUrl}/admin/login`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ password }),
            });
            if (res.ok) {
                setIsAuthenticated(true);
                fetchLogs();
                fetchPrompt();
            } else {
                alert("Invalid Password");
            }
        } catch (e) {
            alert("Backend error");
        }
    };

    const fetchLogs = async () => {
        const res = await fetch(`${baseUrl}/admin/logs?password=${password}`);
        if (res.ok) setLogs(await res.json());
    };

    const fetchPrompt = async () => {
        const res = await fetch(`${baseUrl}/admin/system-prompt?password=${password}`);
        if (res.ok) {
            const data = await res.json();
            setSystemPrompt(data.system_prompt);
        }
    };

    const updatePrompt = async () => {
        const res = await fetch(`${baseUrl}/admin/system-prompt`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ new_prompt: systemPrompt, password }),
        });
        if (res.ok) setStatus("Prompt updated successfully!");
        else setStatus("Failed to update prompt.");
    };

    if (!isAuthenticated) {
        return (
            <div className="flex h-screen items-center justify-center bg-gray-50">
                <div className="p-8 bg-white shadow-lg rounded-lg w-96">
                    <h1 className="text-xl font-bold mb-4 text-[#158CBA]">Admin Login</h1>
                    <input
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        placeholder="Enter Admin Password"
                        className="w-full p-2 border rounded mb-4"
                    />
                    <button onClick={login} className="w-full bg-[#158CBA] text-white p-2 rounded hover:bg-blue-600">
                        Login
                    </button>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gray-50 font-sans">
            <nav className="bg-white border-b px-8 py-4 flex justify-between items-center shadow-sm">
                <h1 className="text-xl font-bold text-[#158CBA]">eCOMET Admin</h1>
                <button onClick={() => setIsAuthenticated(false)} className="text-red-500">Logout</button>
            </nav>

            <div className="p-8 max-w-6xl mx-auto">
                <div className="flex space-x-4 mb-6">
                    <button
                        onClick={() => setActiveTab("logs")}
                        className={clsx("px-4 py-2 rounded", activeTab === "logs" ? "bg-[#158CBA] text-white" : "bg-white text-gray-700 hover:bg-gray-100")}
                    >
                        Chat Logs
                    </button>
                    <button
                        onClick={() => setActiveTab("prompt")}
                        className={clsx("px-4 py-2 rounded", activeTab === "prompt" ? "bg-[#158CBA] text-white" : "bg-white text-gray-700 hover:bg-gray-100")}
                    >
                        System Prompt
                    </button>
                </div>

                {activeTab === "logs" && (
                    <div className="bg-white p-6 rounded shadow">
                        <h2 className="text-lg font-bold mb-4">User Interactions</h2>
                        <div className="space-y-4">
                            {logs.length === 0 ? <p className="text-gray-500">No logs yet.</p> : logs.slice().reverse().map((log, i) => (
                                <div key={i} className="border-b pb-4">
                                    <p className="text-xs text-gray-400">{log.timestamp}</p>
                                    <p className="font-semibold text-[#158CBA]">User: {log.user}</p>
                                    <p className="text-gray-700 mt-1">Bot: {log.bot}</p>
                                </div>
                            ))}
                        </div>
                    </div>
                )}

                {activeTab === "prompt" && (
                    <div className="bg-white p-6 rounded shadow">
                        <h2 className="text-lg font-bold mb-4">Edit System Persona</h2>
                        <textarea
                            value={systemPrompt}
                            onChange={(e) => setSystemPrompt(e.target.value)}
                            className="w-full h-96 p-4 border rounded font-mono text-sm leading-relaxed"
                        />
                        <div className="mt-4 flex items-center justify-between">
                            <button onClick={updatePrompt} className="bg-[#158CBA] text-white px-6 py-2 rounded hover:bg-blue-600">
                                Update Prompt
                            </button>
                            {status && <span className="text-green-600">{status}</span>}
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}
