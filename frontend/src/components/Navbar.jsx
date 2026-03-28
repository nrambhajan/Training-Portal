import { useNavigate, Link } from "react-router-dom";
import { LogOut } from "lucide-react";

export default function Navbar({ role }) {
  const navigate = useNavigate();

  function logout() {
    localStorage.clear();
    navigate("/login");
  }

  const adminLinks = [
    { to: "/admin", label: "Dashboard" },
    { to: "/admin/modules", label: "Modules" },
    { to: "/admin/trainees", label: "Trainees" },
  ];

  const traineeLinks = [
    { to: "/trainee", label: "My Labs" },
    { to: "/trainee/leaderboard", label: "Leaderboard" },
  ];
  const links = role === "admin" ? adminLinks : traineeLinks;

  return (
    <nav className="bg-white border-b border-gray-200 px-6 py-2 flex items-center justify-between shadow-sm">
      <div className="flex items-center gap-4">
        {/* Logo */}
        <Link to={role === "admin" ? "/admin" : "/trainee"}>
          <img src="/logo.svg" alt="SupportSages" className="h-7 w-auto" />
        </Link>

        {/* Divider */}
        <div className="h-5 w-px bg-gray-300" />

        {/* Nav links */}
        <span className="flex gap-1">
          {links.map((l) => (
            <Link
              key={l.to}
              to={l.to}
              className="px-3 py-1.5 rounded text-sm text-gray-600 hover:text-gray-900 hover:bg-gray-100 transition font-medium"
            >
              {l.label}
            </Link>
          ))}
        </span>
      </div>

      <button
        onClick={logout}
        className="flex items-center gap-1.5 text-sm text-gray-500 hover:text-gray-900 transition"
      >
        <LogOut size={15} /> Logout
      </button>
    </nav>
  );
}
