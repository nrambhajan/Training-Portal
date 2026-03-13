import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import api from "../../api";
import Navbar from "../../components/Navbar";
import toast from "react-hot-toast";
import {
  Plus, Pencil, Trash2, ArrowLeft, Terminal,
  List, FileText, ChevronDown, ChevronUp, BookOpen,
} from "lucide-react";

const TYPE_META = {
  mcq:          { label: "MCQ",           icon: <List size={13} />,     color: "bg-blue-100 text-blue-700" },
  practical:    { label: "Practical",     icon: <Terminal size={13} />, color: "bg-green-100 text-green-700" },
  output:       { label: "Cmd Output",    icon: <FileText size={13} />, color: "bg-orange-100 text-orange-700" },
  short_answer: { label: "Theory",        icon: <BookOpen size={13} />, color: "bg-violet-100 text-violet-700" },
};

const BLANK_FORM = {
  type: "short_answer",
  text: "",
  options: ["", "", "", ""],
  correct_answer: "",
  verify_command: "",
  verify_expected: "",
  verify_type: "exit_code",
  points: 1,
  order: 0,
  hint: "",
};

/* ── Modal wrapper ─────────────────────────────────────────────────────────── */
function Modal({ title, onClose, children }) {
  return (
    <div className="fixed inset-0 bg-black/40 flex items-start justify-center z-50 overflow-y-auto py-8 px-4">
      <div className="bg-white rounded-2xl shadow-2xl w-full max-w-lg p-6 my-auto">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">{title}</h3>
        {children}
        <button
          onClick={onClose}
          className="mt-3 text-sm text-gray-400 hover:text-gray-700"
        >
          Cancel
        </button>
      </div>
    </div>
  );
}

/* ── Question form (shared for add + edit) ─────────────────────────────────── */
function QuestionForm({ form, setForm }) {
  const set = (k, v) => setForm((f) => ({ ...f, [k]: v }));

  return (
    <div className="flex flex-col gap-4 max-h-[70vh] overflow-y-auto pr-1">

      {/* ── Type selector ──────────────────────────────────────────────── */}
      <div>
        <label className="block text-xs font-semibold text-gray-500 uppercase tracking-wide mb-1">
          Question Type
        </label>
        <select
          className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-gray-800"
          value={form.type}
          onChange={(e) => set("type", e.target.value)}
        >
          <option value="short_answer">Theory — Written Answer</option>
          <option value="mcq">MCQ — Multiple Choice</option>
          <option value="practical">Practical — SSH Task Verification</option>
          <option value="output">Command Output — Paste &amp; Check</option>
        </select>
      </div>

      {/* ── Question text ─────────────────────────────────────────────── */}
      <div>
        <label className="block text-xs font-semibold text-gray-500 uppercase tracking-wide mb-1">
          Question / Task Description
        </label>
        <textarea
          rows={4}
          className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm resize-none focus:outline-none focus:ring-2 focus:ring-gray-800"
          placeholder="Type the question here…"
          value={form.text}
          onChange={(e) => set("text", e.target.value)}
        />
      </div>

      {/* ── Theory: Model Answer ──────────────────────────────────────── */}
      {form.type === "short_answer" && (
        <div>
          <label className="block text-xs font-semibold text-gray-500 uppercase tracking-wide mb-1">
            Model Answer{" "}
            <span className="normal-case font-normal text-gray-400">
              (shown to you when grading)
            </span>
          </label>
          <textarea
            rows={5}
            className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm resize-none focus:outline-none focus:ring-2 focus:ring-violet-500 bg-violet-50"
            placeholder="Type the expected / correct answer here…"
            value={form.correct_answer}
            onChange={(e) => set("correct_answer", e.target.value)}
          />
        </div>
      )}

      {/* ── MCQ options ───────────────────────────────────────────────── */}
      {form.type === "mcq" && (
        <div>
          <label className="block text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2">
            Options — select the correct one
          </label>
          <div className="flex flex-col gap-2">
            {(form.options || ["", "", "", ""]).map((opt, i) => (
              <div key={i} className="flex items-center gap-2">
                <input
                  type="radio"
                  name="correct"
                  checked={String(form.correct_answer) === String(i)}
                  onChange={() => set("correct_answer", String(i))}
                  className="accent-gray-900"
                />
                <input
                  type="text"
                  placeholder={`Option ${i + 1}`}
                  className={`flex-1 border rounded-lg px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-gray-800 ${
                    String(form.correct_answer) === String(i)
                      ? "border-green-400 bg-green-50"
                      : "border-gray-300"
                  }`}
                  value={opt}
                  onChange={(e) => {
                    const opts = [...(form.options || ["", "", "", ""])];
                    opts[i] = e.target.value;
                    set("options", opts);
                  }}
                />
              </div>
            ))}
          </div>
        </div>
      )}

      {/* ── Practical SSH task ─────────────────────────────────────────── */}
      {form.type === "practical" && (
        <>
          <div>
            <label className="block text-xs font-semibold text-gray-500 uppercase tracking-wide mb-1">
              Verification Command{" "}
              <span className="normal-case font-normal text-gray-400">(run on trainee's server)</span>
            </label>
            <input
              type="text"
              placeholder="e.g.  id john  or  systemctl is-active nginx"
              className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm font-mono focus:outline-none focus:ring-2 focus:ring-gray-800"
              value={form.verify_command}
              onChange={(e) => set("verify_command", e.target.value)}
            />
          </div>
          <div>
            <label className="block text-xs font-semibold text-gray-500 uppercase tracking-wide mb-1">
              Pass Condition
            </label>
            <select
              className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm"
              value={form.verify_type}
              onChange={(e) => set("verify_type", e.target.value)}
            >
              <option value="exit_code">Exit code 0 (command succeeds)</option>
              <option value="contains">Output contains text</option>
              <option value="regex">Output matches regex pattern</option>
            </select>
          </div>
          {form.verify_type !== "exit_code" && (
            <div>
              <label className="block text-xs font-semibold text-gray-500 uppercase tracking-wide mb-1">
                Expected Output
              </label>
              <input
                type="text"
                placeholder={form.verify_type === "regex" ? "e.g.  uid=\\d+  " : "e.g.  john  "}
                className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm font-mono focus:outline-none focus:ring-2 focus:ring-gray-800"
                value={form.verify_expected}
                onChange={(e) => set("verify_expected", e.target.value)}
              />
            </div>
          )}
        </>
      )}

      {/* ── Command Output ─────────────────────────────────────────────── */}
      {form.type === "output" && (
        <>
          <div>
            <label className="block text-xs font-semibold text-gray-500 uppercase tracking-wide mb-1">
              Match Method
            </label>
            <select
              className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm"
              value={form.verify_type}
              onChange={(e) => set("verify_type", e.target.value)}
            >
              <option value="contains">Output contains text</option>
              <option value="regex">Output matches regex</option>
            </select>
          </div>
          <div>
            <label className="block text-xs font-semibold text-gray-500 uppercase tracking-wide mb-1">
              Expected Pattern
            </label>
            <input
              type="text"
              className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm font-mono focus:outline-none focus:ring-2 focus:ring-gray-800"
              value={form.verify_expected}
              onChange={(e) => set("verify_expected", e.target.value)}
            />
          </div>
        </>
      )}

      {/* ── Points / Order / Hint ─────────────────────────────────────── */}
      <div className="grid grid-cols-2 gap-3">
        <div>
          <label className="block text-xs font-semibold text-gray-500 uppercase tracking-wide mb-1">Points</label>
          <input
            type="number" min={0.5} step={0.5}
            className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm"
            value={form.points}
            onChange={(e) => set("points", parseFloat(e.target.value))}
          />
        </div>
        <div>
          <label className="block text-xs font-semibold text-gray-500 uppercase tracking-wide mb-1">Order #</label>
          <input
            type="number" min={0}
            className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm"
            value={form.order}
            onChange={(e) => set("order", parseInt(e.target.value))}
          />
        </div>
      </div>

      <div>
        <label className="block text-xs font-semibold text-gray-500 uppercase tracking-wide mb-1">
          Hint <span className="normal-case font-normal text-gray-400">(optional — shown to trainee)</span>
        </label>
        <input
          type="text"
          className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm"
          placeholder="e.g. Use the 'free' command"
          value={form.hint}
          onChange={(e) => set("hint", e.target.value)}
        />
      </div>
    </div>
  );
}

/* ── Question card (admin list view) ───────────────────────────────────────── */
function QuestionCard({ q, idx, onEdit, onDelete }) {
  const [expanded, setExpanded] = useState(false);
  const meta = TYPE_META[q.type] || TYPE_META.short_answer;

  return (
    <div className="bg-white rounded-xl border border-gray-200 px-5 py-4 hover:border-gray-300 transition">
      <div className="flex items-start justify-between gap-4">
        <div className="flex-1 min-w-0">
          {/* Header row */}
          <div className="flex flex-wrap items-center gap-2 mb-2">
            <span className="text-xs text-gray-400 font-mono">#{idx + 1}</span>
            <span className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs font-medium ${meta.color}`}>
              {meta.icon} {meta.label}
            </span>
            <span className="text-xs text-gray-400">{q.points} pt{q.points !== 1 ? "s" : ""}</span>
          </div>

          {/* Question text */}
          <p className="text-sm text-gray-800 leading-relaxed">{q.text}</p>

          {/* MCQ options preview */}
          {q.type === "mcq" && q.options && (
            <ul className="mt-2 flex flex-col gap-1">
              {q.options.map((o, i) => (
                <li
                  key={i}
                  className={`text-xs px-2 py-1 rounded-md ${
                    String(q.correct_answer) === String(i)
                      ? "bg-green-50 text-green-700 font-semibold"
                      : "text-gray-500"
                  }`}
                >
                  {String(q.correct_answer) === String(i) ? "✓ " : "○ "}{o}
                </li>
              ))}
            </ul>
          )}

          {/* Practical verify command */}
          {q.type === "practical" && q.verify_command && (
            <div className="mt-2 text-xs text-gray-500 font-mono bg-gray-50 border border-gray-200 px-3 py-1.5 rounded-lg">
              $ {q.verify_command}
              <span className="text-gray-400 font-sans ml-2">({q.verify_type})</span>
            </div>
          )}

          {/* Theory: collapsible model answer */}
          {q.type === "short_answer" && q.correct_answer && (
            <div className="mt-2">
              <button
                onClick={() => setExpanded((v) => !v)}
                className="inline-flex items-center gap-1 text-xs text-violet-600 hover:text-violet-800 font-medium"
              >
                {expanded ? <ChevronUp size={13} /> : <ChevronDown size={13} />}
                {expanded ? "Hide model answer" : "Show model answer"}
              </button>
              {expanded && (
                <div className="mt-1.5 text-xs text-gray-600 bg-violet-50 border border-violet-100 rounded-lg px-3 py-2 leading-relaxed whitespace-pre-wrap">
                  {q.correct_answer}
                </div>
              )}
            </div>
          )}

          {/* Hint */}
          {q.hint && (
            <div className="mt-2 text-xs text-amber-600 italic">
              💡 {q.hint}
            </div>
          )}
        </div>

        {/* Action buttons */}
        <div className="flex items-center gap-1 shrink-0">
          <button
            onClick={() => onEdit(q)}
            title="Edit question"
            className="p-2 text-gray-400 hover:text-blue-600 rounded-lg hover:bg-blue-50 transition"
          >
            <Pencil size={15} />
          </button>
          <button
            onClick={() => onDelete(q.id)}
            title="Delete question"
            className="p-2 text-gray-400 hover:text-red-500 rounded-lg hover:bg-red-50 transition"
          >
            <Trash2 size={15} />
          </button>
        </div>
      </div>
    </div>
  );
}

/* ── Main page ──────────────────────────────────────────────────────────────── */
export default function AdminQuestions() {
  const { moduleId } = useParams();
  const navigate = useNavigate();
  const [questions, setQuestions] = useState([]);
  const [moduleTitle, setModuleTitle] = useState("");
  const [showForm, setShowForm] = useState(false);
  const [editing, setEditing] = useState(null);
  const [form, setForm] = useState(BLANK_FORM);
  const [search, setSearch] = useState("");

  async function load() {
    const [{ data: qs }, { data: mods }] = await Promise.all([
      api.get(`/modules/${moduleId}/questions`),
      api.get("/modules"),
    ]);
    setQuestions(qs);
    const mod = mods.find((m) => String(m.id) === String(moduleId));
    if (mod) setModuleTitle(mod.title);
  }

  useEffect(() => { load(); }, [moduleId]);

  async function save() {
    if (!form.text.trim()) {
      toast.error("Question text is required");
      return;
    }
    try {
      if (editing) {
        await api.put(`/questions/${editing.id}`, form);
        toast.success("Question updated ✓");
      } else {
        await api.post(`/modules/${moduleId}/questions`, form);
        toast.success("Question added ✓");
      }
      setShowForm(false);
      setEditing(null);
      setForm(BLANK_FORM);
      load();
    } catch {
      toast.error("Failed to save — check the form");
    }
  }

  async function del(id) {
    if (!confirm("Delete this question? This cannot be undone.")) return;
    await api.delete(`/questions/${id}`);
    toast.success("Question deleted");
    load();
  }

  function openEdit(q) {
    setEditing(q);
    setForm({
      type:             q.type,
      text:             q.text,
      options:          q.options?.length ? q.options : ["", "", "", ""],
      correct_answer:   q.correct_answer ?? "",
      verify_command:   q.verify_command  || "",
      verify_expected:  q.verify_expected || "",
      verify_type:      q.verify_type     || "exit_code",
      points:           q.points,
      order:            q.order,
      hint:             q.hint || "",
    });
    setShowForm(true);
  }

  function openAdd() {
    setEditing(null);
    setForm({ ...BLANK_FORM, order: questions.length });
    setShowForm(true);
  }

  const filtered = questions.filter(
    (q) =>
      !search ||
      q.text.toLowerCase().includes(search.toLowerCase()) ||
      (q.correct_answer || "").toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar role="admin" />

      <div className="max-w-4xl mx-auto px-6 py-8">
        {/* ── Header ── */}
        <div className="flex items-center gap-3 mb-6">
          <button
            onClick={() => navigate("/admin/modules")}
            className="text-gray-400 hover:text-gray-700 transition"
          >
            <ArrowLeft size={20} />
          </button>
          <div className="flex-1">
            <div className="text-xs text-gray-400 uppercase tracking-wide">Module</div>
            <h2 className="text-2xl font-bold text-gray-900">{moduleTitle}</h2>
          </div>
          <span className="text-sm text-gray-500">{questions.length} question{questions.length !== 1 ? "s" : ""}</span>
          <button
            onClick={openAdd}
            className="flex items-center gap-2 bg-gray-900 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-gray-700 transition"
          >
            <Plus size={16} /> Add Question
          </button>
        </div>

        {/* ── Search ── */}
        {questions.length > 5 && (
          <input
            type="text"
            placeholder="Search questions or model answers…"
            className="w-full border border-gray-300 rounded-xl px-4 py-2.5 text-sm mb-4 focus:outline-none focus:ring-2 focus:ring-gray-800"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        )}

        {/* ── Question list ── */}
        <div className="flex flex-col gap-3">
          {filtered.map((q, idx) => (
            <QuestionCard
              key={q.id}
              q={q}
              idx={search ? questions.indexOf(q) : idx}
              onEdit={openEdit}
              onDelete={del}
            />
          ))}
          {filtered.length === 0 && (
            <div className="text-center py-16 text-gray-400">
              {search ? "No questions match your search." : "No questions yet. Click 'Add Question' to start."}
            </div>
          )}
        </div>
      </div>

      {/* ── Edit / Add modal ── */}
      {showForm && (
        <Modal
          title={editing ? `Edit Question #${questions.indexOf(editing) + 1}` : "New Question"}
          onClose={() => { setShowForm(false); setEditing(null); }}
        >
          <QuestionForm form={form} setForm={setForm} />
          <button
            onClick={save}
            className="mt-4 w-full bg-gray-900 text-white rounded-lg py-2.5 text-sm font-semibold hover:bg-gray-700 transition"
          >
            {editing ? "Update Question" : "Add Question"}
          </button>
        </Modal>
      )}
    </div>
  );
}
