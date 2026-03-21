import React from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider } from './context/AuthContext.jsx'
import Navbar from './components/Navbar.jsx'
import ProtectedRoute from './components/ProtectedRoute.jsx'

// Public pages
import Home from './pages/Home.jsx'
import Login from './pages/Login.jsx'
import Standings from './pages/Standings.jsx'
import Matches from './pages/Matches.jsx'

// Admin pages
import Dashboard from './pages/Dashboard.jsx'
import Teams from './pages/Teams.jsx'
import Players from './pages/Players.jsx'
import Stats from './pages/Stats.jsx'
import Articles from './pages/Articles.jsx'

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Navbar />
        <main style={{ flex: 1 }}>
          <Routes>
            {/* ── Public routes ─────────────────────────────────────────── */}
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<Login />} />
            <Route path="/standings" element={<Standings />} />
            <Route path="/matches" element={<Matches />} />

            {/* ── Admin routes (protected) ───────────────────────────────── */}
            <Route path="/admin/dashboard" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
            <Route path="/admin/teams"     element={<ProtectedRoute><Teams /></ProtectedRoute>} />
            <Route path="/admin/players"   element={<ProtectedRoute><Players /></ProtectedRoute>} />
            <Route path="/admin/matches"   element={<ProtectedRoute><Matches /></ProtectedRoute>} />
            <Route path="/admin/standings" element={<ProtectedRoute><Standings /></ProtectedRoute>} />
            <Route path="/admin/stats"     element={<ProtectedRoute><Stats /></ProtectedRoute>} />
            <Route path="/admin/articles"  element={<ProtectedRoute><Articles /></ProtectedRoute>} />

            {/* Legacy redirects */}
            <Route path="/dashboard" element={<Navigate to="/admin/dashboard" replace />} />

            {/* 404 fallback */}
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </main>
      </BrowserRouter>
    </AuthProvider>
  )
}
