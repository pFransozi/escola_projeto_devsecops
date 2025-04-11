import { useEffect, useState } from 'react';

function App() {
  const [mensagem, setMensagem] = useState("Conectando...");

  useEffect(() => {
    fetch("http://localhost:5000/api/hello")
      .then((res) => res.json())
      .then((data) => setMensagem(data.message))
      .catch(() => setMensagem("Erro ao conectar com backend."));
  }, []);

  return (
    <div style={{ textAlign: "center", marginTop: "100px" }}>
      <h1>Sistema Escolar – Tela de Login</h1>
      <p>{mensagem}</p>
    </div>
  );
}

export default App;
