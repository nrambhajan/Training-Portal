#!/bin/bash
# Start both backend and frontend in development mode

echo "==> Starting Linux Training Portal"

# Backend
cd backend
python3 -m venv venv 2>/dev/null || true
source venv/bin/activate
pip install -r requirements.txt -q
uvicorn main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!
echo "  Backend PID: $BACKEND_PID (http://localhost:8000)"
cd ..

# Frontend
cd frontend
npm run dev &
FRONTEND_PID=$!
echo "  Frontend PID: $FRONTEND_PID (http://localhost:5173)"
cd ..

echo ""
echo "  Admin login: admin / admin123"
echo "  Press Ctrl+C to stop both"
echo ""

trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT TERM
wait
