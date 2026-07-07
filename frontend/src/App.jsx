import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/Login';
import Register from './pages/Register'; // <-- Importe aqui
import Dashboard from './pages/Dashboard';
import CreateLesson from './pages/CreateLesson';

const DashboardTemp = () => (
  <div className="flex h-screen items-center justify-center bg-slate-900 text-white">
    <h1 className="text-3xl">Sucesso! Você está no Dashboard.</h1>
  </div>
);

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} /> {/* <-- Adicione a rota aqui */}
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="*" element={<Navigate to="/login" replace />} />
        <Route path="/create-lesson" element={<CreateLesson />} />
      </Routes>
    </BrowserRouter>
  );
}