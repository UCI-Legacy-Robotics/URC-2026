'use client';

export default function DigitalKeyboardStatus() {
  return (
    <div style={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      <h3 style={{ fontSize: '1.1rem', color: '#A0A0A0', margin: '0 0 10px 0', textTransform: 'uppercase' }}>Digital Keyboard Status</h3>
      <div style={{ flexGrow: 1, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '10px', width: '100%' }}>
           {/* Mock key indicators */}
          {['W', 'A', 'S', 'D', 'ARM', 'CAM'].map(key => (
            <div key={key} style={{ background: '#222', padding: '8px', textAlign: 'center', borderRadius: '4px', border: '1px solid #333', color: '#888', fontFamily: 'monospace' }}>
              {key}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}