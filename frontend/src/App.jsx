import React from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider } from './context/AuthContext.jsx'
import Navbar from './components/Navbar'
import ProtectedRoute from './components/ProtectedRoute.jsx'
import Dashboard from './pages/Dashboard'
import Teams from './pages/Teams'
import Players from './pages/Players'
import Matches from './pages/Matches'
import Standings from './pages/Standings'
import Stats from './pages/Stats'
import Articles from './pages/Articles'
import Login from './pages/Login'

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Navbar />
        <main style={{ flex: 1 }}>
          <Routes>
            {/* ── Public routes ─────────────────────────────────────────── */}
            <Route path="/login"     element={<Login />} />
            <Route path="/standings" element={<Standings />} />
            <Route path="/matches"   element={<Matches />} />

            {/* ── Admin routes (protected) ───────────────────────────────── */}
            <Route path="/dashboard" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
            <Route path="/teams"     element={<ProtectedRoute><Teams /></ProtectedRoute>} />
            <Route path="/players"   element={<ProtectedRoute><Players /></ProtectedRoute>} />
            <Route path="/articles"  element={<ProtectedRoute><Articles /></ProtectedRoute>} />
            <Route path="/stats"     element={<ProtectedRoute><Stats /></ProtectedRoute>} />

            {/* Default: redirect to standings or dashboard based on auth */}
            <Route path="/" element={<Navigate to="/standings" replace />} />
            <Route path="*" element={<Navigate to="/standings" replace />} />
          </Routes>
        </main>
      </BrowserRouter>
    </AuthProvider>
  )
}
