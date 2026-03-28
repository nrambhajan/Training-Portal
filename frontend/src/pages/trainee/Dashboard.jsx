import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../../api";
import Navbar from "../../components/Navbar";
import { BookOpen, ChevronRight, CheckCircle, Lock, Trophy, TrendingUp } from "lucide-react";

export default function TraineeDashboard() {
  const [modules, setModules] = useState([]);
  const [progress, setProgress] = useState({});
  const [unlockStatus, setUnlockStatus] = useState({});
  const navigate = useNavigate();
  const name = localStorage.getItem("name") || "Trainee";

  useEffect(() => {
    Promise.all([
      api.get("/my/modules"),
      api.get("/my/progress"),
      api.get("/my/modules/unlock-status"),
    ]).then(([m, p, u]) => {
      setModules(m.data);
      const pMap = {};
      p.data.forEach((row) => { pMap[row.module_id] = row; });
      setProgress(pMap);
      const uMap = {};
      u.data.forEach((row) => { uMap[row.module_id] = row; });
      setUnlockStatus(uMap);
    });
  }, []);

  // Overall stats
  const totalScore = Object.values(progress).reduce((s, p) => s + (p.score || 0), 0);
  const totalMax = Object.values(progress).reduce((s, p) => s + (p.max_score || 0), 0);
  const totalPct = totalMax > 0 ? Math.round(totalScore / totalMax * 100) : 0;
  const totalCorrect = Object.values(progress).reduce((s, p) => s + (p.correct || 0), 0);
  const totalQuestions = Object.values(progress).reduce((s, p) => s + (p.total_questions || 0), 0);

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar role="trainee" />
      <div className="max-w-3xl mx-auto px-6 py-10">
        <h2 className="text-2xl font-bold text-gray-900 mb-1">Welcome back, {name}</h2>
        <p className="text-gray-500 text-sm mb-6">Pick a module below to work on your tasks.</p>

        {/* Overall score card */}
        <div className="bg-white rounded-xl border border-gray-200 p-6 mb-8 flex items-center justify-between">
          <div>
            <div className="text-sm text-gray-500 mb-1">Overall Progress</div>
            <div className="text-3xl font-bold text-gray-900">{totalPct}%</div>
            <div className="text-xs text-gray-400 mt-1">
              {totalCorrect}/{totalQuestions} correct · {totalScore}/{totalMax} points
            </div>
          </div>
          <div className="flex gap-3">
            <button
              onClick={() => navigate("/trainee/leaderboard")}
              className="flex items-center gap-2 bg-yellow-50 text-yellow-700 px-4 py-2 rounded-lg text-sm font-medium hover:bg-yellow-100 transition border border-yellow-200"
            >
              <Trophy size={16} /> Leaderboard
            </button>
          </div>
        </div>

        <div className="flex flex-col gap-4">
          {modules.map((m) => {
            const p = progress[m.id] || {};
            const u = unlockStatus[m.id] || {};
            const pct = p.percent || 0;
            const done = (p.attempted || 0) === (p.total_questions || m.question_count) && m.question_count > 0;
            const locked = u.locked;

            return (
              <div
                key={m.id}
                onClick={() => {
                  if (locked) return;
                  navigate(`/trainee/modules/${m.id}`);
                }}
                className={`bg-white rounded-xl border px-6 py-5 flex items-center gap-4 transition
                  ${locked
                    ? "border-gray-100 opacity-60 cursor-not-allowed"
                    : "border-gray-200 cursor-pointer hover:border-gray-400 hover:shadow-sm"
                  }`}
              >
                <div className={`w-11 h-11 rounded-xl flex items-center justify-center shrink-0 ${
                  locked ? "bg-gray-100" : done ? "bg-green-100" : "bg-purple-50"
                }`}>
                  {locked ? (
                    <Lock size={20} className="text-gray-400" />
                  ) : done ? (
                    <CheckCircle size={22} className="text-green-600" />
                  ) : (
                    <BookOpen size={22} className="text-purple-500" />
                  )}
                </div>
                <div className="flex-1">
                  <div className="font-semibold text-gray-900">{m.title}</div>
                  {locked ? (
                    <div className="text-xs text-red-500 mt-1">
                      Complete previous module with {u.required_pct}% to unlock (currently {u.prev_pct}%)
                    </div>
                  ) : (
                    <>
                      {m.description && <div className="text-sm text-gray-400 mt-0.5">{m.description}</div>}
                      <div className="mt-2 flex items-center gap-2">
                        <div className="flex-1 h-1.5 bg-gray-100 rounded-full overflow-hidden">
                          <div
                            className={`h-1.5 rounded-full transition-all ${pct >= 70 ? "bg-green-500" : "bg-purple-400"}`}
                            style={{ width: `${pct}%` }}
                          />
                        </div>
                        <span className="text-xs text-gray-400">{p.attempted || 0}/{p.total_questions || m.question_count}</span>
                        <span className={`text-xs font-semibold ${pct >= 70 ? "text-green-600" : pct >= 40 ? "text-yellow-600" : "text-gray-400"}`}>
                          {pct}%
                        </span>
                      </div>
                      {m.time_limit && (
                        <div className="text-xs text-orange-500 mt-1">Time limit: {m.time_limit} minutes</div>
                      )}
                    </>
                  )}
                </div>
                {!locked && <ChevronRight size={18} className="text-gray-300 shrink-0" />}
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
