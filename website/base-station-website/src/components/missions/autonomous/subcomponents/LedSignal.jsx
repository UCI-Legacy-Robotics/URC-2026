'use client';

export default function LedSignal() {
  return (
    <div style={{ height: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
      <h3 style={{ fontSize: '1.1rem', color: '#A0A0A0', margin: '0 0 15px 0', textTransform: 'uppercase' }}>Signal for LED</h3>
      
      <div style={{ display: 'flex', gap: '20px', alignItems: 'center' }}>
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '8px' }}>
          <div style={{ 
            width: '30px', 
            height: '30px', 
            borderRadius: '50%', 
            background: '#4ade80', 
            boxShadow: '0 0 15px #4ade80',
            border: '2px solid #fff'
          }}></div>
          <span style={{ color: '#E0E0E0', fontSize: '0.8rem', fontFamily: 'monospace' }}>ACTIVE</span>
        </div>

        <div style={{ height: '40px', width: '1px', background: '#333' }}></div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '5px' }}>
          <span style={{ color: '#aaa', fontSize: '0.9rem' }}>Mode: <strong style={{ color: '#fff' }}>STROBE</strong></span>
          <span style={{ color: '#aaa', fontSize: '0.9rem' }}>Freq: <strong style={{ color: '#fff' }}>2 Hz</strong></span>
        </div>
      </div>
    </div>
  );
}