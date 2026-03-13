import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import toast from "react-hot-toast";
import api from "../api";

export default function Login() {
  const [form, setForm] = useState({ username: "", password: "" });
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  // Handle SSO callback — backend redirects here with ?sso_token=...
  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const ssoToken = params.get("sso_token");
    const role = params.get("role");
    const name = params.get("name");
    const userId = params.get("user_id");
    const error = params.get("sso_error");

    if (error) {
      toast.error(decodeURIComponent(error));
      window.history.replaceState({}, "", "/login");
      return;
    }

    if (ssoToken) {
      localStorage.setItem("token", ssoToken);
      localStorage.setItem("role", role);
      localStorage.setItem("name", name || "");
      localStorage.setItem("user_id", userId || "");
      window.history.replaceState({}, "", "/login");
      navigate(role === "admin" ? "/admin" : "/trainee");
    }
  }, [navigate]);

  async function handleSubmit(e) {
    e.preventDefault();
    setLoading(true);
    try {
      const resp = await api.post("/auth/login", form);
      const data = resp.data;
      localStorage.setItem("token", data.access_token);
      localStorage.setItem("role", data.role);
      localStorage.setItem("name", data.full_name || "");
      localStorage.setItem("user_id", String(data.user_id || ""));
      window.location.href = data.role === "admin" ? "/admin" : "/trainee";
    } catch (err) {
      console.error("Login error:", err);
      if (err.response && err.response.status === 401) {
        toast.error("Invalid username or password");
      } else {
        toast.error("Login failed: " + (err.message || "Unknown error"));
      }
    } finally {
      setLoading(false);
    }
  }

  function handleMicrosoftSSO() {
    window.location.href = "/api/auth/microsoft";
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="bg-white rounded-2xl shadow-lg p-8 w-full max-w-sm border border-gray-100">

        {/* Logo */}
        <div className="flex justify-center mb-6">
          <img src="/logo.svg" alt="SupportSages" className="h-10 w-auto" />
        </div>

        <h1 className="text-xl font-bold text-gray-900 text-center mb-1">
          Linux Training Portal
        </h1>
        <p className="text-gray-400 text-sm text-center mb-6">Sign in to continue</p>

        {/* Microsoft SSO Button */}
        <button
          onClick={handleMicrosoftSSO}
          className="w-full flex items-center justify-center gap-3 border border-gray-300 rounded-lg py-2.5 px-4 text-sm font-medium text-gray-700 hover:bg-gray-50 transition mb-4 shadow-sm"
        >
          {/* Microsoft official logo */}
          <svg width="18" height="18" viewBox="0 0 21 21" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect x="1" y="1" width="9" height="9" fill="#F25022"/>
            <rect x="11" y="1" width="9" height="9" fill="#7FBA00"/>
            <rect x="1" y="11" width="9" height="9" fill="#00A4EF"/>
            <rect x="11" y="11" width="9" height="9" fill="#FFB900"/>
          </svg>
          Sign in with Microsoft
        </button>

        {/* Divider */}
        <div className="flex items-center gap-3 my-4">
          <div className="flex-1 h-px bg-gray-200" />
          <span className="text-xs text-gray-400">or use admin credentials</span>
          <div className="flex-1 h-px bg-gray-200" />
        </div>

        {/* Username / Password form (admin only) */}
        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Username</label>
            <input
              type="text"
              required
              autoFocus
              className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-[#1F9DD9]"
              value={form.username}
              onChange={(e) => setForm({ ...form, username: e.target.value })}
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Password</label>
            <input
              type="password"
              required
              className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-[#1F9DD9]"
              value={form.password}
              onChange={(e) => setForm({ ...form, password: e.target.value })}
            />
          </div>
          <button
            type="submit"
            disabled={loading}
            className="bg-gray-900 text-white rounded-lg py-2 text-sm font-semibold hover:bg-gray-700 transition disabled:opacity-50"
          >
            {loading ? "Signing in…" : "Sign in"}
          </button>
        </form>
      </div>
    </div>
  );
}
