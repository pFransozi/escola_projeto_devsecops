import React from 'react';

function DashboardCard({ title, count }) {
    return (
        <div style={{ border: '1px solid #ccc', padding: '1rem', borderRadius: '8px' }}>
            <h4>{title}</h4>
            <p style={{ fontSize: '1.5rem', fontWeight: 'bold' }}>{count}</p>
        </div>
    )
}

export default DashboardCard;