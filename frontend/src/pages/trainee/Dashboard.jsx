import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../../api";
import Navbar from "../../components/Navbar";
import { BookOpen, ChevronRight, CheckCircle } from "lucide-react";

export default function TraineeDashboard() {
  const [modules, setModules] = useState([]);
  const [progress, setProgress] = useState({});
  const navigate = useNavigate();
  const name = localStorage.getItem("name") || "Trainee";

  useEffect(() => {
    Promise.all([api.get("/my/modules"), api.get("/my/progress")]).then(([m, p]) => {
      setModules(m.data);
      const map = {};
      p.data.forEach((row) => { map[row.module_id] = row; });
      setProgress(map);
    });
  }, []);

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar role="trainee" />
      <div className="max-w-3xl mx-auto px-6 py-10">
        <h2 className="text-2xl font-bold text-gray-900 mb-1">Welcome back, {name} 👋</h2>
        <p className="text-gray-500 text-sm mb-8">Pick a module below to work on your tasks.</p>

        <div className="flex flex-col gap-4">
          {modules.map((m) => {
            const p = progress[m.id] || {};
            const pct = p.percent || 0;
            const done = (p.attempted || 0) === (p.total_questions || m.question_count) && m.question_count > 0;
            return (
              <div
                key={m.id}
                onClick={() => navigate(`/trainee/modules/${m.id}`)}
                className="bg-white rounded-xl border border-gray-200 px-6 py-5 flex items-center gap-4 cursor-pointer hover:border-gray-400 hover:shadow-sm transition"
              >
                <div className={`w-11 h-11 rounded-xl flex items-center justify-center shrink-0 ${done ? "bg-green-100" : "bg-purple-50"}`}>
                  {done ? <CheckCircle size={22} className="text-green-600" /> : <BookOpen size={22} className="text-purple-500" />}
                </div>
                <div className="flex-1">
                  <div className="font-semibold text-gray-900">{m.title}</div>
                  {m.description && <div className="text-sm text-gray-400 mt-0.5">{m.description}</div>}
                  {/* Progress bar */}
                  <div className="mt-2 flex items-center gap-2">
                    <div className="flex-1 h-1.5 bg-gray-100 rounded-full overflow-hidden">
                      <div
                        className={`h-1.5 rounded-full transition-all ${pct >= 70 ? "bg-green-500" : "bg-purple-400"}`}
                        style={{ width: `${pct}%` }}
                      />
                    </div>
                    <span className="text-xs text-gray-400">{p.attempted || 0}/{p.total_questions || m.question_count}</span>
                  </div>
                </div>
                <ChevronRight size={18} className="text-gray-300 shrink-0" />
              </div>
            );
          })}
          {modules.length === 0 && (
            <div className="text-center py-16 text-gray-400">No modules assigned yet. Check back soon.</div>
          )}
        </div>
      </div>
    </div>
  );
}
