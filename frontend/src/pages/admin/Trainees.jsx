import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../../api";
import Navbar from "../../components/Navbar";
import toast from "react-hot-toast";
import { Plus, Pencil, Trash2, Server, ChevronRight } from "lucide-react";

const BLANK = {
  username: "", password: "", full_name: "", email: "",
  server_ip: "", ssh_user: "", ssh_password: "", ssh_port: 22,
};

function Modal({ title, onClose, children }) {
  return (
    <div className="fixed inset-0 bg-black/40 flex items-center justify-center z-50 overflow-y-auto py-8">
      <div className="bg-white rounded-2xl shadow-2xl w-full max-w-md mx-4 p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">{title}</h3>
        {children}
        <button onClick={onClose} className="mt-3 text-sm text-gray-400 hover:text-gray-700">Cancel</button>
      </div>
    </div>
  );
}

export default function AdminTrainees() {
  const [trainees, setTrainees] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [editing, setEditing] = useState(null);
  const [form, setForm] = useState(BLANK);
  const navigate = useNavigate();

  async function load() {
    const { data } = await api.get("/trainees");
    setTrainees(data);
  }

  useEffect(() => { load(); }, []);

  const setF = (k) => (e) => setForm((f) => ({ ...f, [k]: e.target.value }));

  async function save() {
    try {
      const payload = { ...form };
      payload.ssh_port = parseInt(payload.ssh_port, 10) || 22;
      if (editing && !payload.password) delete payload.password;
      if (editing && !payload.ssh_password) delete payload.ssh_password;
      if (editing) {
        await api.put(`/trainees/${editing.id}`, payload);
        toast.success("Trainee updated");
      } else {
        await api.post("/trainees", payload);
        toast.success("Trainee added");
      }
      setShowForm(false);
      setEditing(null);
      setForm(BLANK);
      load();
    } catch (err) {
      toast.error(err.response?.data?.detail || "Failed to save");
    }
  }

  async function del(id) {
    if (!confirm("Delete this trainee and all their attempts?")) return;
    await api.delete(`/trainees/${id}`);
    toast.success("Deleted");
    load();
  }

  function openEdit(t) {
    setEditing(t);
    setForm({
      username: t.username, password: "",
      full_name: t.full_name || "", email: t.email || "",
      server_ip: t.server_ip || "", ssh_user: t.ssh_user || "",
      ssh_password: "", ssh_port: t.ssh_port || 22,
    });
    setShowForm(true);
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar role="admin" />
      <div className="max-w-4xl mx-auto px-6 py-8">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-bold text-gray-900">Trainees</h2>
          <button
            onClick={() => { setEditing(null); setForm(BLANK); setShowForm(true); }}
            className="flex items-center gap-2 bg-gray-900 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-gray-700 transition"
          >
            <Plus size={16} /> Add Trainee
          </button>
        </div>

        <div className="flex flex-col gap-3">
          {trainees.map((t) => (
            <div key={t.id} className="bg-white rounded-xl border border-gray-200 px-5 py-4 flex items-center justify-between hover:border-gray-300 transition">
              <div className="flex items-center gap-3">
                <div className="w-9 h-9 rounded-full bg-gray-900 text-white flex items-center justify-center text-sm font-bold">
                  {(t.full_name || t.username)[0].toUpperCase()}
                </div>
                <div>
                  <div className="font-semibold text-gray-900">{t.full_name || t.username}</div>
                  <div className="text-xs text-gray-400">@{t.username}</div>
                </div>
              </div>
              <div className="flex items-center gap-4">
                {t.server_ip ? (
                  <div className="flex items-center gap-1 text-xs text-gray-500 font-mono">
                    <Server size={12} className="text-green-500" /> {t.server_ip}:{t.ssh_port || 22}
                  </div>
                ) : (
                  <span className="text-xs text-amber-500">No server configured</span>
                )}
                <button onClick={() => openEdit(t)} className="p-2 text-gray-400 hover:text-gray-700 rounded-lg hover:bg-gray-100 transition"><Pencil size={15} /></button>
                <button onClick={() => del(t.id)} className="p-2 text-gray-400 hover:text-red-500 rounded-lg hover:bg-red-50 transition"><Trash2 size={15} /></button>
                <button onClick={() => navigate(`/admin/trainees/${t.id}`)} className="p-2 text-gray-400 hover:text-gray-900 rounded-lg hover:bg-gray-100 transition"><ChevronRight size={18} /></button>
              </div>
            </div>
          ))}
          {trainees.length === 0 && (
            <div className="text-center py-16 text-gray-400">No trainees yet.</div>
          )}
        </div>
      </div>

      {showForm && (
        <Modal title={editing ? "Edit Trainee" : "Add Trainee"} onClose={() => { setShowForm(false); setEditing(null); }}>
          <div className="flex flex-col gap-3 max-h-[65vh] overflow-y-auto pr-1">
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-xs font-medium text-gray-600 mb-1">Full Name</label>
                <input className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm" value={form.full_name} onChange={setF("full_name")} />
              </div>
              <div>
                <label className="block text-xs font-medium text-gray-600 mb-1">Username *</label>
                <input className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm" value={form.username} onChange={setF("username")} disabled={!!editing} />
              </div>
            </div>
            <div>
              <label className="block text-xs font-medium text-gray-600 mb-1">{editing ? "New Password (leave blank to keep)" : "Password *"}</label>
              <input type="password" className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm" value={form.password} onChange={setF("password")} />
            </div>
            <div>
              <label className="block text-xs font-medium text-gray-600 mb-1">Email</label>
              <input type="email" className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm" value={form.email} onChange={setF("email")} />
            </div>
            <hr className="my-1" />
            <p className="text-xs text-gray-500 font-medium">Server Credentials (for task verification)</p>
            <div className="grid grid-cols-3 gap-2">
              <div className="col-span-2">
                <label className="block text-xs font-medium text-gray-600 mb-1">Server IP</label>
                <input className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm font-mono" placeholder="192.168.1.10" value={form.server_ip} onChange={setF("server_ip")} />
              </div>
              <div>
                <label className="block text-xs font-medium text-gray-600 mb-1">SSH Port</label>
                <input type="number" className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm" value={form.ssh_port} onChange={setF("ssh_port")} />
              </div>
            </div>
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-xs font-medium text-gray-600 mb-1">SSH Username</label>
                <input className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm font-mono" value={form.ssh_user} onChange={setF("ssh_user")} />
              </div>
              <div>
                <label className="block text-xs font-medium text-gray-600 mb-1">SSH Password</label>
                <input type="password" className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm" value={form.ssh_password} onChange={setF("ssh_password")} />
              </div>
            </div>
          </div>
          <button onClick={save} className="mt-4 w-full bg-gray-900 text-white rounded-lg py-2 text-sm font-semibold hover:bg-gray-700 transition">
            {editing ? "Update" : "Add Trainee"}
          </button>
        </Modal>
      )}
    </div>
  );
}
