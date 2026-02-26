'use client';

export default function TaskStatuses() {
  return (
    <div style={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      <h3 style={{ fontSize: '1.1rem', color: '#A0A0A0', margin: '0 0 10px 0', textTransform: 'uppercase' }}>Task Statuses</h3>
      <div style={{ flexGrow: 1, overflowY: 'auto' }}>
        <ul style={{ listStyle: 'none', padding: 0, margin: 0, color: '#E0E0E0' }}>
          <li style={{ marginBottom: '8px', display: 'flex', justifyContent: 'space-between' }}>
            <span>Alignment Check</span> <span style={{ color: '#4ade80' }}>[ OK ]</span>
          </li>
          <li style={{ marginBottom: '8px', display: 'flex', justifyContent: 'space-between' }}>
            <span>Tool Deployment</span> <span style={{ color: '#FFD200' }}>[ IN PROG ]</span>
          </li>
        </ul>
      </div>
    </div>
  );
}