import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import DashboardCard from '../components/dashboardCard';

function HomePage() {
  const [data, setData] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const user = JSON.parse(localStorage.getItem('user'));
    if (!user) {
      navigate('/');
    }
    fetch(`${process.env.REACT_APP_API_URL}/dashboard`)
      .then(res => res.json())
      .then(setData)
      .catch(console.error);
  }, [navigate]);

  return (
    <div style={{ padding: '2rem' }}>
      <h2>Página Principal</h2>
      {data ? (
        <div style={{ display: 'flex', gap: '1rem' }}>
          <DashboardCard title="Total de Usuários" count={data.users} />
          <DashboardCard title="Admins" count={data.admins} />
          <DashboardCard title="Professores" count={data.teachers} />
          <DashboardCard title="Alunos" count={data.students} />
        </div>
      ) : (
        <p>Carregando dados...</p>
      )}
    </div>
  );
}

export default HomePage;