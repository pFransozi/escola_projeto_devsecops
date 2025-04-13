import React, { useState } from "react";

export default function RegisterPage() {
  const [formData, setFormData] = useState({
    nome: "",
    ultimo_nome: "",
    login: "",
    senha: "",
    email: "",
    data_nascimento: "",
    sexo: "",
    cpf: "",
    endereco: "",
    tipo: 1, // padrão: secretaria
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await fetch("http://localhost:5000/api/usuarios", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });
      const data = await res.json();
      if (res.ok) {
        alert("Usuário cadastrado com sucesso!");
        setFormData({ ...formData, senha: "", login: "" }); // limpa
      } else {
        alert(data.message || "Erro ao cadastrar usuário.");
      }
    } catch (err) {
      alert("Erro de rede ao cadastrar.");
      console.error(err);
    }
  };

  return (
    <div>
      <h2>Cadastro de Usuário</h2>
      <form onSubmit={handleSubmit} style={{ maxWidth: "500px" }}>
        <input name="nome" placeholder="Nome" onChange={handleChange} required />
        <input name="ultimo_nome" placeholder="Último nome" onChange={handleChange} />
        <input name="login" placeholder="Login" onChange={handleChange} required />
        <input name="senha" placeholder="Senha" type="password" onChange={handleChange} required />
        <input name="email" placeholder="Email" onChange={handleChange} />
        <input name="data_nascimento" placeholder="Data de nascimento (YYYY-MM-DD)" onChange={handleChange} required />
        <select name="sexo" onChange={handleChange} required>
          <option value="">Sexo</option>
          <option value="M">Masculino</option>
          <option value="F">Feminino</option>
        </select>
        <input name="cpf" placeholder="CPF (somente números)" onChange={handleChange} required />
        <input name="endereco" placeholder="Endereço" onChange={handleChange} required />
        <select name="tipo" onChange={handleChange}>
          <option value={1}>Secretaria</option>
          <option value={2}>Professor</option>
          <option value={0}>Administrador</option>
        </select>

        <button type="submit">Cadastrar</button>
      </form>
    </div>
  );
}
