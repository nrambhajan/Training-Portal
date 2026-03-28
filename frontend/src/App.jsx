import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Login from "./pages/Login";
import AdminDashboard from "./pages/admin/Dashboard";
import AdminModules from "./pages/admin/Modules";
import AdminQuestions from "./pages/admin/Questions";
import AdminTrainees from "./pages/admin/Trainees";
import AdminTraineeDetail from "./pages/admin/TraineeDetail";
import TraineeDashboard from "./pages/trainee/Dashboard";
import TraineeLab from "./pages/trainee/Lab";
import TraineeLeaderboard from "./pages/trainee/Leaderboard";

function ProtectedRoute({ children, role }) {
  const token = localStorage.getItem("token");
  const userRole = localStorage.getItem("role");
  if (!token) return <Navigate to="/login" replace />;
  if (role && userRole !== role) {
    return <Navigate to={userRole === "admin" ? "/admin" : "/trainee"} replace />;
  }
  return children;
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/admin" element={<ProtectedRoute role="admin"><AdminDashboard /></ProtectedRoute>} />
        <Route path="/admin/modules" element={<ProtectedRoute role="admin"><AdminModules /></ProtectedRoute>} />
        <Route path="/admin/modules/:moduleId/questions" element={<ProtectedRoute role="admin"><AdminQuestions /></ProtectedRoute>} />
        <Route path="/admin/trainees" element={<ProtectedRoute role="admin"><AdminTrainees /></ProtectedRoute>} />
        <Route path="/admin/trainees/:traineeId" element={<ProtectedRoute role="admin"><AdminTraineeDetail /></ProtectedRoute>} />
        <Route path="/trainee" element={<ProtectedRoute role="trainee"><TraineeDashboard /></ProtectedRoute>} />
        <Route path="/trainee/modules/:moduleId" element={<ProtectedRoute role="trainee"><TraineeLab /></ProtectedRoute>} />
        <Route path="/trainee/leaderboard" element={<ProtectedRoute role="trainee"><TraineeLeaderboard /></ProtectedRoute>} />
        <Route path="*" element={<Navigate to="/login" replace />} />
      </Routes>
    </BrowserRouter>
  );
}
