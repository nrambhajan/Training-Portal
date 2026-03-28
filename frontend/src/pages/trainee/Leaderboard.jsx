import { useEffect, useState } from "react";
import api from "../../api";
import Navbar from "../../components/Navbar";
import { Trophy, Medal, TrendingUp } from "lucide-react";

export default function Leaderboard() {
  const [data, setData] = useState([]);
  const myId = Number(localStorage.getItem("user_id"));

  useEffect(() => {
    api.get("/dashboard/leaderboard").then((r) => setData(r.data));
  }, []);

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar role="trainee" />
      <div className="max-w-2xl mx-auto px-6 py-10">
        <div className="flex items-center gap-3 mb-8">
          <Trophy size={28} className="text-yellow-500" />
          <h2 className="text-2xl font-bold text-gray-900">Leaderboard</h2>
        </div>

        <div className="bg-white rounded-xl border border-gray-200 overflow-hidden">
          {data.map((t, idx) => {
            const isMe = t.trainee_id === myId;
            const rank = idx + 1;
            return (
              <div
                key={t.trainee_id}
                className={`flex items-center gap-4 px-6 py-4 border-b border-gray-50 last:border-0 transition
                  ${isMe ? "bg-blue-50 border-blue-100" : "hover:bg-gray-50"}`}
              >
                {/* Rank */}
                <div className="w-10 text-center shrink-0">
                  {rank === 1 ? (
                    <span className="text-2xl">🥇</span>
                  ) : rank === 2 ? (
                    <span className="text-2xl">🥈</span>
                  ) : rank === 3 ? (
                    <span className="text-2xl">🥉</span>
                  ) : (
                    <span className="text-lg font-bold text-gray-400">#{rank}</span>
                  )}
                </div>

                {/* Name */}
                <div className="flex-1">
                  <div className={`font-semibold ${isMe ? "text-blue-700" : "text-gray-900"}`}>
                    {t.name} {isMe && <span className="text-xs font-normal text-blue-500">(You)</span>}
                  </div>
                  <div className="text-xs text-gray-400">
                    {t.correct}/{t.total_questions} correct · {t.attempted} attempted
                  </div>
                </div>

                {/* Score */}
                <div className="text-right">
                  <div className={`text-lg font-bold ${
                    t.percent >= 70 ? "text-green-600" : t.percent >= 40 ? "text-yellow-600" : "text-red-500"
                  }`}>
                    {t.percent}%
                  </div>
                  <div className="text-xs text-gray-400">{t.score}/{t.max_score}</div>
                </div>
              </div>
            );
          })}
          {data.length === 0 && (
            <div className="px-6 py-12 text-center text-gray-400">No trainees yet.</div>
          )}
        </div>
      </div>
    </div>
  );
}
