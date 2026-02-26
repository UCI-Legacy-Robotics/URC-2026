'use client';

export default function TimerWidget({ course1, course2 }) {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
      <h2 style={{ fontSize: '1.2rem', color: '#A0A0A0', margin: '0 0 1rem 0', textTransform: 'uppercase', letterSpacing: '1px' }}>
        Time Remaining
      </h2>
      
      <div style={{ flexGrow: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center', gap: '1rem' }}>
        
        {course1 && (
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '10px 15px', background: '#1E1E1E', borderRadius: '6px', borderLeft: '3px solid #0064A4' }}>
            <span style={{ color: '#E0E0E0', fontSize: '1.1rem', fontWeight: '500' }}>Course 1:</span>
            <span style={{ fontFamily: 'monospace', color: '#FFD200', fontSize: '1.4rem', fontWeight: 'bold' }}>
              {course1}
            </span>
          </div>
        )}

        {course2 && (
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '10px 15px', background: '#1E1E1E', borderRadius: '6px', borderLeft: '3px solid #0064A4' }}>
            <span style={{ color: '#E0E0E0', fontSize: '1.1rem', fontWeight: '500' }}>Course 2:</span>
            <span style={{ fontFamily: 'monospace', color: '#FFD200', fontSize: '1.4rem', fontWeight: 'bold' }}>
              {course2}
            </span>
          </div>
        )}

      </div>
    </div>
  );
}