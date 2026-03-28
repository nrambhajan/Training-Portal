import { useEffect, useState, useRef } from "react";
import { useParams, useNavigate } from "react-router-dom";
import api from "../../api";
import Navbar from "../../components/Navbar";
import toast from "react-hot-toast";
import {
  ArrowLeft, CheckCircle, XCircle, Loader2, Terminal,
  List, FileText, Lightbulb, RefreshCw, Clock, AlertTriangle, Link2
} from "lucide-react";

// ── Timer Component ──────────────────────────────────────────────────────────

function Timer({ minutes, onExpire }) {
  const [secondsLeft, setSecondsLeft] = useState(minutes * 60);
  const intervalRef = useRef(null);

  useEffect(() => {
    intervalRef.current = setInterval(() => {
      setSecondsLeft((prev) => {
        if (prev <= 1) {
          clearInterval(intervalRef.current);
          onExpire?.();
          return 0;
        }
        return prev - 1;
      });
    }, 1000);
    return () => clearInterval(intervalRef.current);
  }, []);

  const mins = Math.floor(secondsLeft / 60);
  const secs = secondsLeft % 60;
  const urgent = secondsLeft < 300; // less than 5 mins

  return (
    <div className={`flex items-center gap-2 px-3 py-1.5 rounded-lg text-sm font-mono font-bold
      ${urgent ? "bg-red-100 text-red-700 animate-pulse" : "bg-orange-50 text-orange-700"}`}>
      <Clock size={16} />
      {String(mins).padStart(2, "0")}:{String(secs).padStart(2, "0")}
    </div>
  );
}

// ── Question Cards ──────────────────────────────────────────────────────────

function ShortAnswerCard({ question, attempt, onSubmit, attemptsLeft }) {
  const [text, setText] = useState("");
  const [loading, setLoading] = useState(false);

  async function submit() {
    if (!text.trim()) return toast.error("Write your answer first");
    setLoading(true);
    await onSubmit({ question_id: question.id, submitted_answer: text });
    setLoading(false);
  }

  const submitted = !!attempt;
  const pending = attempt && attempt.is_correct === null;

  return (
    <div className="flex flex-col gap-3">
      {attempt?.submitted_answer && (
        <div className={`rounded-lg border px-4 py-3 text-sm whitespace-pre-wrap
          ${pending ? "border-yellow-200 bg-yellow-50 text-yellow-800" :
            attempt.is_correct ? "border-green-300 bg-green-50 text-green-800" :
            "border-red-200 bg-red-50 text-red-700"}`}>
          <div className="text-xs font-semibold mb-1 text-gray-400">Your answer:</div>
          {attempt.submitted_answer}
          {pending && <div className="mt-2 text-xs text-yellow-600 font-medium">Pending trainer review</div>}
          {attempt.admin_notes && (
            <div className="mt-2 text-xs text-blue-600 bg-blue-50 rounded px-2 py-1">
              Trainer feedback: {attempt.admin_notes}
            </div>
          )}
        </div>
      )}
      {!submitted && attemptsLeft !== 0 && (
        <>
          <textarea
            rows={5}
            placeholder="Type your answer here..."
            className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-gray-800 resize-none"
            value={text}
            onChange={(e) => setText(e.target.value)}
          />
          <button
            onClick={submit}
            disabled={loading}
            className="self-start flex items-center gap-2 bg-gray-900 text-white px-5 py-2 rounded-lg text-sm font-medium hover:bg-gray-700 transition disabled:opacity-50"
          >
            {loading && <Loader2 size={14} className="animate-spin" />} Submit Answer
          </button>
        </>
      )}
    </div>
  );
}

function Badge({ type }) {
  const map = {
    mcq: { label: "MCQ", cls: "bg-blue-100 text-blue-700" },
    practical: { label: "Practical Task", cls: "bg-green-100 text-green-700" },
    output: { label: "Command Output", cls: "bg-orange-100 text-orange-700" },
    short_answer: { label: "Theory", cls: "bg-violet-100 text-violet-700" },
  };
  const m = map[type] || {};
  return <span className={`text-xs font-medium px-2 py-0.5 rounded-full ${m.cls}`}>{m.label}</span>;
}

function StatusBadge({ attempt }) {
  if (!attempt) return <span className="text-xs text-gray-400">Not attempted</span>;
  if (attempt.is_correct === null) return <span className="flex items-center gap-1 text-xs text-yellow-600"><Clock size={13} /> Pending review</span>;
  if (attempt.is_correct) return <span className="flex items-center gap-1 text-xs text-green-600"><CheckCircle size={13} /> Correct</span>;
  return <span className="flex items-center gap-1 text-xs text-red-500"><XCircle size={13} /> Incorrect</span>;
}

function MCQCard({ question, attempt, onSubmit, attemptsLeft }) {
  const [selected, setSelected] = useState(null);
  const [loading, setLoading] = useState(false);

  async function submit() {
    if (selected === null) return toast.error("Select an option first");
    setLoading(true);
    await onSubmit({ question_id: question.id, submitted_answer: String(selected) });
    setLoading(false);
  }

  const locked = attempt?.is_correct || attemptsLeft === 0;

  return (
    <div className="flex flex-col gap-3">
      <div className="flex flex-col gap-2">
        {question.options?.map((opt, i) => {
          const isChosen = attempt && String(attempt.submitted_answer) === String(i);
          const isCorrect = attempt?.is_correct && isChosen;
          const isWrong = !attempt?.is_correct && isChosen;
          return (
            <label
              key={i}
              className={`flex items-center gap-3 border rounded-lg px-4 py-3 cursor-pointer transition text-sm
                ${locked ? "cursor-default" : "hover:border-gray-400"}
                ${isCorrect ? "border-green-400 bg-green-50 text-green-800" :
                  isWrong ? "border-red-300 bg-red-50 text-red-700" :
                  selected === i ? "border-gray-800 bg-gray-50" : "border-gray-200"}`}
            >
              <input
                type="radio"
                name={`q${question.id}`}
                disabled={!!locked}
                checked={selected === i}
                onChange={() => setSelected(i)}
                className="accent-gray-900"
              />
              {opt}
            </label>
          );
        })}
      </div>
      {!locked && (
        <button
          onClick={submit}
          disabled={loading || selected === null}
          className="self-start flex items-center gap-2 bg-gray-900 text-white px-5 py-2 rounded-lg text-sm font-medium hover:bg-gray-700 transition disabled:opacity-50"
        >
          {loading && <Loader2 size={14} className="animate-spin" />} Submit
        </button>
      )}
      {attempt?.admin_notes && (
        <div className="rounded-lg border border-blue-200 bg-blue-50 px-4 py-3 text-sm text-blue-800">
          <span className="font-semibold text-xs text-blue-600">Trainer feedback:</span> {attempt.admin_notes}
        </div>
      )}
    </div>
  );
}

function PracticalCard({ question, attempt, onVerify }) {
  const [loading, setLoading] = useState(false);

  async function verify() {
    setLoading(true);
    await onVerify(question.id);
    setLoading(false);
  }

  return (
    <div className="flex flex-col gap-3">
      <p className="text-sm text-gray-500">Complete this task on your server, then click <strong>Verify</strong> — the system will SSH in and check automatically.</p>

      {attempt?.server_output && (
        <div className={`rounded-lg border px-4 py-3 text-xs font-mono whitespace-pre-wrap
          ${attempt.is_correct ? "border-green-300 bg-green-50 text-green-800" : "border-red-200 bg-red-50 text-red-700"}`}>
          {attempt.is_correct ? "Task verified successfully!" : "Verification failed. Try again after completing the task."}
        </div>
      )}

      {attempt?.admin_notes && (
        <div className="rounded-lg border border-blue-200 bg-blue-50 px-4 py-3 text-sm text-blue-800">
          <span className="font-semibold text-xs text-blue-600">Trainer feedback:</span> {attempt.admin_notes}
        </div>
      )}

      <div className="flex items-center gap-2">
        <button
          onClick={verify}
          disabled={loading}
          className="flex items-center gap-2 bg-green-700 text-white px-5 py-2 rounded-lg text-sm font-medium hover:bg-green-600 transition disabled:opacity-50"
        >
          {loading ? <Loader2 size={14} className="animate-spin" /> : <Terminal size={14} />}
          {attempt ? "Re-Verify" : "Verify Task"}
        </button>
        {attempt && <RefreshCw size={14} className="text-gray-400" />}
        {attempt && <span className="text-xs text-gray-400">You can re-verify as many times as needed</span>}
      </div>
    </div>
  );
}

function OutputCard({ question, attempt, onSubmit, attemptsLeft }) {
  const [text, setText] = useState("");
  const [loading, setLoading] = useState(false);

  async function submit() {
    if (!text.trim()) return toast.error("Paste your command output first");
    setLoading(true);
    await onSubmit({ question_id: question.id, submitted_answer: text });
    setLoading(false);
  }

  const locked = attempt?.is_correct || attemptsLeft === 0;

  return (
    <div className="flex flex-col gap-3">
      <p className="text-sm text-gray-500">Run the command on your server and paste the full output below.</p>
      {attempt?.submitted_answer && (
        <div className={`rounded-lg border px-4 py-3 text-xs font-mono whitespace-pre-wrap
          ${attempt.is_correct ? "border-green-300 bg-green-50 text-green-800" : "border-red-200 bg-red-50 text-red-700"}`}>
          {attempt.submitted_answer}
        </div>
      )}
      {!locked && (
        <>
          <textarea
            rows={5}
            placeholder="Paste command output here..."
            className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm font-mono focus:outline-none focus:ring-2 focus:ring-gray-800 resize-none"
            value={text}
            onChange={(e) => setText(e.target.value)}
          />
          <button
            onClick={submit}
            disabled={loading}
            className="self-start flex items-center gap-2 bg-gray-900 text-white px-5 py-2 rounded-lg text-sm font-medium hover:bg-gray-700 transition disabled:opacity-50"
          >
            {loading && <Loader2 size={14} className="animate-spin" />} Submit Output
          </button>
        </>
      )}
      {attempt?.admin_notes && (
        <div className="rounded-lg border border-blue-200 bg-blue-50 px-4 py-3 text-sm text-blue-800">
          <span className="font-semibold text-xs text-blue-600">Trainer feedback:</span> {attempt.admin_notes}
        </div>
      )}
    </div>
  );
}

// ── Main Lab Component ──────────────────────────────────────────────────────

export default function TraineeLab() {
  const { moduleId } = useParams();
  const navigate = useNavigate();
  const [items, setItems] = useState([]);
  const [moduleTitle, setModuleTitle] = useState("");
  const [moduleData, setModuleData] = useState(null);
  const [openHint, setOpenHint] = useState(null);
  const [expired, setExpired] = useState(false);

  async function load() {
    const [{ data: qs }, { data: mods }] = await Promise.all([
      api.get(`/my/modules/${moduleId}/questions`),
      api.get("/my/modules"),
    ]);
    setItems(qs);
    const mod = mods.find((m) => String(m.id) === String(moduleId));
    if (mod) {
      setModuleTitle(mod.title);
      setModuleData(mod);
    }
  }

  useEffect(() => { load(); }, [moduleId]);

  async function handleSubmit(payload) {
    if (expired) return toast.error("Time is up! You can no longer submit answers.");
    try {
      await api.post("/attempts/submit", payload);
      toast.success("Answer submitted!");
      load();
    } catch (err) {
      toast.error(err.response?.data?.detail || "Submission failed");
    }
  }

  async function handleVerify(questionId) {
    if (expired) return toast.error("Time is up!");
    try {
      const { data } = await api.post(`/attempts/verify/${questionId}`);
      if (data.is_correct) toast.success("Task verified - correct!");
      else toast.error("Verification failed. Check and try again.");
      load();
    } catch (err) {
      toast.error(err.response?.data?.detail || "Verification failed");
    }
  }

  const correct = items.filter((i) => i.attempt?.is_correct).length;
  const total = items.length;

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar role="trainee" />
      <div className="max-w-3xl mx-auto px-6 py-8">
        {/* Header */}
        <div className="flex items-center gap-3 mb-6">
          <button onClick={() => navigate("/trainee")} className="text-gray-400 hover:text-gray-700"><ArrowLeft size={20} /></button>
          <div className="flex-1">
            <h2 className="text-2xl font-bold text-gray-900">{moduleTitle}</h2>
            <div className="text-sm text-gray-400">{correct}/{total} completed</div>
          </div>
          <div className="flex items-center gap-4">
            {moduleData?.time_limit && !expired && (
              <Timer minutes={moduleData.time_limit} onExpire={() => {
                setExpired(true);
                toast.error("Time is up! No more submissions allowed.", { duration: 5000 });
              }} />
            )}
            {expired && (
              <div className="flex items-center gap-1 text-red-600 text-sm font-bold">
                <AlertTriangle size={16} /> Time Expired
              </div>
            )}
            <div className="text-right">
              <div className="text-2xl font-bold text-gray-900">{total > 0 ? Math.round(correct / total * 100) : 0}%</div>
              <div className="text-xs text-gray-400">Score</div>
            </div>
          </div>
        </div>

        {/* Progress bar */}
        <div className="h-2 bg-gray-200 rounded-full mb-4 overflow-hidden">
          <div
            className="h-2 bg-green-500 rounded-full transition-all"
            style={{ width: total > 0 ? `${(correct / total) * 100}%` : "0%" }}
          />
        </div>

        {/* Resource links */}
        {moduleData?.resources && moduleData.resources.length > 0 && (
          <div className="mb-6 bg-blue-50 border border-blue-200 rounded-lg px-4 py-3">
            <div className="text-xs font-semibold text-blue-700 mb-1 flex items-center gap-1">
              <Link2 size={13} /> Study Resources
            </div>
            <div className="flex flex-wrap gap-3">
              {moduleData.resources.map((r, i) => (
                <a
                  key={i}
                  href={r.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-sm text-blue-600 hover:text-blue-800 underline"
                >
                  {r.title || r.url}
                </a>
              ))}
            </div>
          </div>
        )}

        {/* Questions */}
        <div className="flex flex-col gap-6">
          {items.map(({ question: q, attempt, attempt_count }, idx) => {
            const maxAttempts = q.max_attempts;
            const attemptsLeft = maxAttempts ? Math.max(0, maxAttempts - (attempt_count || 0)) : null;

            return (
              <div key={q.id} className={`bg-white rounded-xl border-2 transition
                ${attempt?.is_correct ? "border-green-200" :
                  attempt?.is_correct === false ? "border-red-100" :
                  attempt?.is_correct === null ? "border-yellow-100" : "border-gray-200"}`}>
                <div className="px-6 py-4 border-b border-gray-100 flex items-center justify-between gap-3">
                  <div className="flex items-center gap-2">
                    <span className="text-sm font-bold text-gray-400">Q{idx + 1}</span>
                    <Badge type={q.type} />
                    <span className="text-xs text-gray-400">{q.points} pt{q.points !== 1 ? "s" : ""}</span>
                    {maxAttempts && (
                      <span className={`text-xs px-1.5 py-0.5 rounded ${
                        attemptsLeft === 0 ? "bg-red-100 text-red-600" : "bg-gray-100 text-gray-500"
                      }`}>
                        {attemptsLeft === 0 ? "No attempts left" : `${attemptsLeft}/${maxAttempts} left`}
                      </span>
                    )}
                  </div>
                  <StatusBadge attempt={attempt} />
                </div>

                <div className="px-6 py-5">
                  <p className="text-gray-900 font-medium mb-4">{q.text}</p>

                  {q.type === "mcq" && (
                    <MCQCard question={q} attempt={attempt} onSubmit={handleSubmit} attemptsLeft={attemptsLeft} />
                  )}
                  {q.type === "practical" && (
                    <PracticalCard question={q} attempt={attempt} onVerify={handleVerify} />
                  )}
                  {q.type === "output" && (
                    <OutputCard question={q} attempt={attempt} onSubmit={handleSubmit} attemptsLeft={attemptsLeft} />
                  )}
                  {q.type === "short_answer" && (
                    <ShortAnswerCard question={q} attempt={attempt} onSubmit={handleSubmit} attemptsLeft={attemptsLeft} />
                  )}

                  {q.hint && (
                    <div className="mt-4">
                      <button
                        onClick={() => setOpenHint(openHint === q.id ? null : q.id)}
                        className="flex items-center gap-1 text-xs text-amber-600 hover:text-amber-800 transition"
                      >
                        <Lightbulb size={13} /> {openHint === q.id ? "Hide hint" : "Show hint"}
                      </button>
                      {openHint === q.id && (
                        <div className="mt-2 text-sm text-amber-700 bg-amber-50 border border-amber-200 rounded-lg px-4 py-2">
                          {q.hint}
                        </div>
                      )}
                    </div>
                  )}
                </div>
              </div>
            );
          })}
          {items.length === 0 && (
            <div className="text-center py-16 text-gray-400">No questions in this module yet.</div>
          )}
        </div>
      </div>
    </div>
  );
}
