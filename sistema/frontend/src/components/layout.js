import React from "react";
import { Link, Outlet } from "react-router-dom";
import "./layout.css";

export default function Layout() {
  return (
    <div className="layout">
      <header className="layout-header">
        <h1>🎓 Sistema Escolar</h1>
      </header>
      <nav className="layout-nav">
        <Link to="/home">Início</Link>
        <Link to="/register">Cadastrar Usuário</Link>
        {/* Adicione outras opções aqui */}
      </nav>
      <main className="layout-main">
        <Outlet />
      </main>
    </div>
  );
}
