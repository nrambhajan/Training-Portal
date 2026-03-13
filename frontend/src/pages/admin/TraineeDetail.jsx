import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import api from "../../api";
import Navbar from "../../components/Navbar";
import toast from "react-hot-toast";
import {
  ArrowLeft, CheckCircle, XCircle, Clock, Terminal, List, FileText,
  ChevronDown, ChevronUp, AlertCircle, ThumbsUp, ThumbsDown, RefreshCw,
} from "lucide-react";

const TYPE_ICON = {
  mcq: <List size={14} className="text-blue-500" />,
  practical: <Terminal size={14} className="text-emerald-500" />,
  output: <FileText size={14} className="text-orange-500" />,
  short_answer: <FileText size={14} className="text-violet-500" />,
};

const TYPE_LABEL = {
  mcq: "MCQ",
  practical: "Practical",
  output: "Output",
  short_answer: "Theory",
};

function StatusBadge({ att }) {
  if (!att) return <span className="inline-flex items-center gap-1 text-xs text-gray-400"><Clock size={14} /> Not attempted</span>;
  if (att.is_correct === null || att.is_correct === undefined)
    return <span className="inline-flex items-center gap-1 text-xs text-amber-500 font-medium"><AlertCircle size={14} /> Pending review</span>;
  if (att.is_correct)
    return <span className="inline-flex items-center gap-1 text-xs text-green-600 font-medium"><CheckCircle size={14} /> Correct</span>;
  return <span className="inline-flex items-center gap-1 text-xs text-red-500 font-medium"><XCircle size={14} /> Incorrect</span>;
}

export default function AdminTraineeDetail() {
  const { traineeId } = useParams();
  const navigate = useNavigate();
  const [data, setData] = useState(null);
  const [expanded, setExpanded] = useState({});
  const [grading, setGrading] = useState({});

  function fetchData() {
    api.get(`/dashboard/trainee/${traineeId}`).then((r) => setData(r.data));
  }

  useEffect(() => { fetchData(); }, [traineeId]);

  if (!data) return <div className="min-h-screen flex items-center justify-center text-gray-400">Loading...</div>;

  const t = data.trainee;
  const allQuestions = data.modules.flatMap((m) => m.questions);
  const totalPts = allQuestions.reduce((s, q) => s + q.points, 0);
  const earnedPts = allQuestions.reduce((s, q) => s + (q.attempt?.score || 0), 0);
  const correct = allQuestions.filter((q) => q.attempt?.is_correct === true).length;
  const pending = allQuestions.filter((q) => q.attempt && (q.attempt.is_correct === null || q.attempt.is_correct === undefined)).length;

  function toggleExpand(qId) {
    setExpanded((prev) => ({ ...prev, [qId]: !prev[qId] }));
  }

  async function handleGrade(attemptId, isCorrect) {
    setGrading((prev) => ({ ...prev, [attemptId]: true }));
    try {
      await api.put(`/dashboard/grade/${attemptId}`, { is_correct: isCorrect });
      toast.success(isCorrect ? "Marked correct" : "Marked incorrect");
      fetchData();
    } catch {
      toast.error("Failed to grade");
    } finally {
      setGrading((prev) => ({ ...prev, [attemptId]: false }));
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar role="admin" />
      <div className="max-w-5xl mx-auto px-6 py-8">
        {/* Header */}
        <div className="flex items-center gap-3 mb-6">
          <button onClick={() => navigate("/admin")} className="text-gray-400 hover:text-gray-700">
            <ArrowLeft size={20} />
          </button>
          <div className="flex-1">
            <h2 className="text-2xl font-bold text-gray-900">{t.full_name || t.username}</h2>
            <div className="text-sm text-gray-400">@{t.username} · Server: {t.server_ip || "not configured"}</div>
          </div>
          <div className="flex gap-6 text-center">
            <div>
              <div className="text-2xl font-bold text-gray-900">
                {earnedPts.toFixed(1)}<span className="text-sm text-gray-400">/{totalPts}</span>
              </div>
              <div className="text-xs text-gray-500">Points</div>
            </div>
            <div>
              <div className={`text-2xl font-bold ${totalPts > 0 && (earnedPts / totalPts) >= 0.7 ? "text-green-600" : "text-gray-900"}`}>
                {totalPts > 0 ? Math.round(earnedPts / totalPts * 100) : 0}%
              </div>
              <div className="text-xs text-gray-500">Score</div>
            </div>
            <div>
              <div className="text-2xl font-bold text-gray-900">{correct}/{allQuestions.length}</div>
              <div className="text-xs text-gray-500">Correct</div>
            </div>
            {pending > 0 && (
              <div>
                <div className="text-2xl font-bold text-amber-500">{pending}</div>
                <div className="text-xs text-gray-500">Pending</div>
              </div>
            )}
          </div>
        </div>

        {/* Modules */}
        {data.modules.map((m) => {
          const mCorrect = m.questions.filter((q) => q.attempt?.is_correct === true).length;
          const mPending = m.questions.filter((q) => q.attempt && (q.attempt.is_correct === null || q.attempt.is_correct === undefined)).length;
          const mEarned = m.questions.reduce((s, q) => s + (q.attempt?.score || 0), 0);
          const mTotal = m.questions.reduce((s, q) => s + q.points, 0);

          return (
            <div key={m.module_id} className="bg-white rounded-xl border border-gray-200 mb-4 overflow-hidden">
              {/* Module header */}
              <div className="px-5 py-3 bg-gray-50 border-b border-gray-100 flex items-center justify-between">
                <span className="font-semibold text-gray-900">{m.module_title}</span>
                <div className="flex items-center gap-4 text-xs">
                  <span className="text-gray-500">{mEarned.toFixed(1)}/{mTotal} pts</span>
                  <span className="text-gray-500">{mCorrect}/{m.questions.length} correct</span>
                  {mPending > 0 && (
                    <span className="bg-amber-100 text-amber-700 px-2 py-0.5 rounded-full font-medium">
                      {mPending} pending
                    </span>
                  )}
                </div>
              </div>

              {/* Questions */}
              <div className="divide-y divide-gray-50">
                {m.questions.map((q) => {
                  const att = q.attempt;
                  const isExpanded = expanded[q.question_id];
                  const canExpand = att && (q.type === "short_answer" || q.type === "output" || q.type === "practical");
                  const isPending = att && (att.is_correct === null || att.is_correct === undefined);

                  return (
                    <div key={q.question_id}>
                      {/* Question row */}
                      <div
                        className={`flex items-center px-5 py-3 text-sm ${canExpand ? "cursor-pointer hover:bg-gray-50" : ""} ${isPending ? "bg-amber-50/50" : ""}`}
                        onClick={() => canExpand && toggleExpand(q.question_id)}
                      >
                        {/* Type */}
                        <div className="w-16 flex items-center gap-1.5">
                          {TYPE_ICON[q.type]}
                          <span className="text-xs text-gray-400">{TYPE_LABEL[q.type]}</span>
                        </div>

                        {/* Question text */}
                        <div className="flex-1 text-gray-800 pr-4 line-clamp-2">{q.text}</div>

                        {/* Status */}
                        <div className="w-36 text-center">
                          <StatusBadge att={att} />
                        </div>

                        {/* Score */}
                        <div className="w-20 text-center font-semibold text-sm">
                          {att ? (
                            <span className={att.is_correct === true ? "text-green-600" : att.is_correct === false ? "text-red-400" : "text-amber-500"}>
                              {att.score ?? "?"}/{q.points}
                            </span>
                          ) : (
                            <span className="text-gray-300">-/{q.points}</span>
                          )}
                        </div>

                        {/* Expand arrow */}
                        <div className="w-8 text-center">
                          {canExpand && (
                            isExpanded
                              ? <ChevronUp size={16} className="text-gray-400 mx-auto" />
                              : <ChevronDown size={16} className="text-gray-400 mx-auto" />
                          )}
                        </div>
                      </div>

                      {/* Expanded detail panel */}
                      {isExpanded && att && (
                        <div className="px-5 py-4 bg-gray-50 border-t border-gray-100">
                          <div className="grid grid-cols-2 gap-4">
                            {/* Trainee's answer */}
                            <div>
                              <div className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2">
                                Trainee's Answer
                              </div>
                              <div className="bg-white border border-gray-200 rounded-lg p-3 text-sm text-gray-700 min-h-[80px] whitespace-pre-wrap">
                                {att.submitted_answer || att.server_output || <span className="text-gray-400 italic">No answer submitted</span>}
                              </div>
                              {att.server_output && att.submitted_answer && (
                                <div className="mt-2">
                                  <div className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-1">Server Output</div>
                                  <div className="bg-gray-900 text-green-400 rounded-lg p-3 text-xs font-mono whitespace-pre-wrap">
                                    {att.server_output}
                                  </div>
                                </div>
                              )}
                            </div>

                            {/* Model answer */}
                            <div>
                              <div className="text-xs font-semibold text-violet-600 uppercase tracking-wide mb-2">
                                Model Answer
                              </div>
                              <div className="bg-violet-50 border border-violet-200 rounded-lg p-3 text-sm text-gray-700 min-h-[80px] whitespace-pre-wrap">
                                {q.correct_answer || <span className="text-gray-400 italic">No model answer set</span>}
                              </div>
                            </div>
                          </div>

                          {/* Grading buttons */}
                          {q.type === "short_answer" && (
                            <div className="mt-4 flex items-center gap-3">
                              {isPending ? (
                                <>
                                  <button
                                    onClick={(e) => { e.stopPropagation(); handleGrade(att.id, true); }}
                                    disabled={grading[att.id]}
                                    className="flex items-center gap-2 bg-green-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-green-700 transition disabled:opacity-50"
                                  >
                                    <ThumbsUp size={16} /> Mark Correct
                                  </button>
                                  <button
                                    onClick={(e) => { e.stopPropagation(); handleGrade(att.id, false); }}
                                    disabled={grading[att.id]}
                                    className="flex items-center gap-2 bg-red-500 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-red-600 transition disabled:opacity-50"
                                  >
                                    <ThumbsDown size={16} /> Mark Incorrect
                                  </button>
                                </>
                              ) : (
                                <div className="flex items-center gap-3">
                                  <span className={`text-sm font-medium ${att.is_correct ? "text-green-600" : "text-red-500"}`}>
                                    {att.is_correct ? "Graded: Correct" : "Graded: Incorrect"}
                                    {att.graded_at && <span className="text-gray-400 font-normal ml-2">({new Date(att.graded_at).toLocaleString()})</span>}
                                  </span>
                                  <button
                                    onClick={(e) => {
                                      e.stopPropagation();
                                      handleGrade(att.id, !att.is_correct);
                                    }}
                                    disabled={grading[att.id]}
                                    className="flex items-center gap-1 text-xs text-gray-500 hover:text-gray-700 border border-gray-300 px-2 py-1 rounded transition disabled:opacity-50"
                                  >
                                    <RefreshCw size={12} /> Re-grade
                                  </button>
                                </div>
                              )}
                            </div>
                          )}
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
