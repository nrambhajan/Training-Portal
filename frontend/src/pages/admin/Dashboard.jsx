import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../../api";
import Navbar from "../../components/Navbar";
import { Users, BookOpen, CheckCircle, XCircle, ChevronRight } from "lucide-react";

export default function AdminDashboard() {
  const [data, setData] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    api.get("/dashboard/overview").then((r) => setData(r.data));
  }, []);

  if (!data) return <div className="min-h-screen flex items-center justify-center text-gray-400">Loading…</div>;

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar role="admin" />
      <div className="max-w-6xl mx-auto px-6 py-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">Dashboard</h2>

        {/* Stats row */}
        <div className="grid grid-cols-3 gap-4 mb-8">
          {[
            { label: "Trainees", value: data.total_trainees, icon: <Users size={20} className="text-blue-500" /> },
            { label: "Modules", value: data.total_modules, icon: <BookOpen size={20} className="text-purple-500" /> },
            { label: "Questions", value: data.total_questions, icon: <CheckCircle size={20} className="text-green-500" /> },
          ].map((s) => (
            <div key={s.label} className="bg-white rounded-xl border border-gray-200 p-5 flex items-center gap-4">
              <div className="bg-gray-100 p-2 rounded-lg">{s.icon}</div>
              <div>
                <div className="text-2xl font-bold text-gray-900">{s.value}</div>
                <div className="text-sm text-gray-500">{s.label}</div>
              </div>
            </div>
          ))}
        </div>

        {/* Trainee table */}
        <div className="bg-white rounded-xl border border-gray-200 overflow-hidden">
          <div className="px-6 py-4 border-b border-gray-100">
            <h3 className="font-semibold text-gray-900">Trainee Progress</h3>
          </div>
          <table className="w-full text-sm">
            <thead className="bg-gray-50 text-gray-500 text-xs uppercase tracking-wide">
              <tr>
                <th className="text-left px-6 py-3">Name</th>
                <th className="text-left px-6 py-3">Server IP</th>
                <th className="text-center px-6 py-3">Attempted</th>
                <th className="text-center px-6 py-3">Correct</th>
                <th className="text-center px-6 py-3">Score</th>
                <th className="text-center px-6 py-3">%</th>
                <th className="px-6 py-3"></th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {data.trainees.map((t) => (
                <tr key={t.trainee_id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 font-medium text-gray-900">{t.trainee_name}</td>
                  <td className="px-6 py-4 text-gray-500 font-mono text-xs">{t.server_ip || "—"}</td>
                  <td className="px-6 py-4 text-center">{t.attempted}/{t.total_questions}</td>
                  <td className="px-6 py-4 text-center">
                    <span className="flex items-center justify-center gap-1">
                      {t.correct > 0 ? <CheckCircle size={14} className="text-green-500" /> : <XCircle size={14} className="text-gray-300" />}
                      {t.correct}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-center font-mono">{t.score}/{t.max_score}</td>
                  <td className="px-6 py-4 text-center">
                    <span className={`font-semibold ${t.percent >= 70 ? "text-green-600" : t.percent >= 40 ? "text-yellow-600" : "text-red-500"}`}>
                      {t.percent}%
                    </span>
                  </td>
                  <td className="px-6 py-4 text-right">
                    <button
                      onClick={() => navigate(`/admin/trainees/${t.trainee_id}`)}
                      className="text-gray-400 hover:text-gray-900 transition"
                    >
                      <ChevronRight size={18} />
                    </button>
                  </td>
                </tr>
              ))}
              {data.trainees.length === 0 && (
                <tr><td colSpan={7} className="px-6 py-8 text-center text-gray-400">No trainees yet. Add some from the Trainees page.</td></tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
