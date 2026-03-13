import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../../api";
import Navbar from "../../components/Navbar";
import toast from "react-hot-toast";
import { Plus, Pencil, Trash2, ChevronRight, BookOpen, Upload } from "lucide-react";

function Modal({ title, onClose, children }) {
  return (
    <div className="fixed inset-0 bg-black/40 flex items-center justify-center z-50">
      <div className="bg-white rounded-2xl shadow-2xl w-full max-w-md p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">{title}</h3>
        {children}
        <button onClick={onClose} className="mt-3 text-sm text-gray-400 hover:text-gray-700">Cancel</button>
      </div>
    </div>
  );
}

export default function AdminModules() {
  const [modules, setModules] = useState([]);
  const [showAdd, setShowAdd] = useState(false);
  const [importing, setImporting] = useState(false);

  async function handleCsvImport(e) {
    const file = e.target.files[0];
    if (!file) return;
    setImporting(true);
    const form = new FormData();
    form.append("file", file);
    try {
      const { data } = await api.post("/import/csv", form, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      toast.success(`Imported ${data.questions_created} questions across ${data.modules_created} module(s)`);
      load();
    } catch (err) {
      toast.error(err.response?.data?.detail || "Import failed");
    } finally {
      setImporting(false);
      e.target.value = "";
    }
  }
  const [editing, setEditing] = useState(null);
  const [form, setForm] = useState({ title: "", description: "" });
  const navigate = useNavigate();

  async function load() {
    const { data } = await api.get("/modules");
    setModules(data);
  }

  useEffect(() => { load(); }, []);

  async function save() {
    try {
      if (editing) {
        await api.put(`/modules/${editing.id}`, form);
        toast.success("Module updated");
      } else {
        await api.post("/modules", form);
        toast.success("Module created");
      }
      setShowAdd(false);
      setEditing(null);
      setForm({ title: "", description: "" });
      load();
    } catch {
      toast.error("Failed to save module");
    }
  }

  async function del(id) {
    if (!confirm("Delete this module and all its questions?")) return;
    await api.delete(`/modules/${id}`);
    toast.success("Deleted");
    load();
  }

  function openEdit(m) {
    setEditing(m);
    setForm({ title: m.title, description: m.description || "" });
    setShowAdd(true);
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar role="admin" />
      <div className="max-w-4xl mx-auto px-6 py-8">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-bold text-gray-900">Modules</h2>
          <button
            onClick={() => { setEditing(null); setForm({ title: "", description: "" }); setShowAdd(true); }}
            className="flex items-center gap-2 bg-gray-900 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-gray-700 transition"
          >
            <Plus size={16} /> New Module
          </button>
          <label className={`flex items-center gap-2 border border-gray-300 text-gray-700 px-4 py-2 rounded-lg text-sm font-medium hover:bg-gray-100 transition cursor-pointer ${importing ? "opacity-50 pointer-events-none" : ""}`}>
            <Upload size={16} /> {importing ? "Importing…" : "Import CSV"}
            <input type="file" accept=".csv" className="hidden" onChange={handleCsvImport} />
          </label>
        </div>

        <div className="flex flex-col gap-3">
          {modules.map((m) => (
            <div key={m.id} className="bg-white rounded-xl border border-gray-200 px-5 py-4 flex items-center justify-between hover:border-gray-300 transition">
              <div className="flex items-center gap-3">
                <BookOpen size={20} className="text-purple-500" />
                <div>
                  <div className="font-semibold text-gray-900">{m.title}</div>
                  <div className="text-sm text-gray-500">{m.description || "No description"} · {m.question_count} question{m.question_count !== 1 ? "s" : ""}</div>
                </div>
              </div>
              <div className="flex items-center gap-2">
                <button onClick={() => openEdit(m)} className="p-2 text-gray-400 hover:text-gray-700 rounded-lg hover:bg-gray-100 transition"><Pencil size={16} /></button>
                <button onClick={() => del(m.id)} className="p-2 text-gray-400 hover:text-red-500 rounded-lg hover:bg-red-50 transition"><Trash2 size={16} /></button>
                <button onClick={() => navigate(`/admin/modules/${m.id}/questions`)} className="p-2 text-gray-400 hover:text-gray-900 rounded-lg hover:bg-gray-100 transition"><ChevronRight size={18} /></button>
              </div>
            </div>
          ))}
          {modules.length === 0 && (
            <div className="text-center py-16 text-gray-400">No modules yet. Create your first one.</div>
          )}
        </div>
      </div>

      {showAdd && (
        <Modal title={editing ? "Edit Module" : "New Module"} onClose={() => { setShowAdd(false); setEditing(null); }}>
          <div className="flex flex-col gap-3">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Title</label>
              <input
                autoFocus
                className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-gray-800"
                value={form.title}
                onChange={(e) => setForm({ ...form, title: e.target.value })}
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Description (optional)</label>
              <textarea
                rows={3}
                className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-gray-800 resize-none"
                value={form.description}
                onChange={(e) => setForm({ ...form, description: e.target.value })}
              />
            </div>
            <button
              onClick={save}
              className="bg-gray-900 text-white rounded-lg py-2 text-sm font-semibold hover:bg-gray-700 transition"
            >
              {editing ? "Update" : "Create"}
            </button>
          </div>
        </Modal>
      )}
    </div>
  );
}
