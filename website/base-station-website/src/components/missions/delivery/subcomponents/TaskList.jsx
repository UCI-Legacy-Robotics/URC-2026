'use client';

export default function TaskList() {
  // Mock data based directly on your wireframe
  const tasks = [
    { id: 1, title: 'Task 1:', desc: 'Open toolbox [black], pick up rock / Open cache, place rock in', pts: '20pt' },
    { id: 2, title: 'Task 2: 20m of GNSS', desc: 'Locate small (5pt) or large (2pt) pieces, deliver to astronaut #1', pts: 'max 30pt' },
    { id: 3, title: 'Task 3:', desc: 'Drone - Read number on sign. Rover - Start cone, go to cone 2, pick up object, deliver to start.', pts: '20pt' },
    { id: 4, title: 'Task 4:', desc: 'Find object in work area, deliver to astronaut #2', pts: '10pt' },
    { id: 5, title: 'Task 5:', desc: 'Get hidden wreckage and deliver to astronaut #2 (comms issues)', pts: '20pt' },
  ];

  return (
    <div style={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      <div style={{ flexGrow: 1, overflowY: 'auto', paddingRight: '10px' }}>
        {tasks.map((task) => (
          <div key={task.id} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '1rem', borderBottom: '1px solid #333', paddingBottom: '0.5rem' }}>
            <div style={{ flex: 1, paddingRight: '1rem' }}>
              <strong style={{ color: '#fff', fontSize: '1.1rem' }}>{task.title}</strong>
              <p style={{ color: '#aaa', margin: '4px 0 0 0', fontSize: '0.9rem', lineHeight: '1.4' }}>{task.desc}</p>
            </div>
            
            <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
              <span style={{ color: '#FFD200', fontWeight: 'bold' }}>{task.pts}</span>
              {/* Checkbox Placeholder */}
              <div style={{ width: '24px', height: '24px', background: 'rgba(244, 114, 182, 0.2)', border: '1px solid #f472b6', borderRadius: '4px' }}></div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}