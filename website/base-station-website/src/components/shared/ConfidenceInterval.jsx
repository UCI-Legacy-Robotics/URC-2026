'use client';

export default function ConfidenceInterval() {
  return (
    <div style={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      <h3 style={{ fontSize: '1.1rem', color: '#A0A0A0', margin: '0 0 10px 0', textTransform: 'uppercase' }}>Image Recognition Confidence</h3>
      <div style={{ flexGrow: 1, display: 'flex', flexDirection: 'column', gap: '12px', justifyContent: 'center' }}>
        
        <div>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '4px', color: '#E0E0E0', fontSize: '0.9rem' }}>
            <span>Primary Target (Wrench)</span>
            <span style={{ color: '#4ade80', fontFamily: 'monospace' }}>94.2%</span>
          </div>
          <div style={{ height: '8px', background: '#222', borderRadius: '4px', overflow: 'hidden' }}>
            <div style={{ width: '94.2%', height: '100%', background: '#4ade80' }}></div>
          </div>
        </div>

        <div>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '4px', color: '#E0E0E0', fontSize: '0.9rem' }}>
            <span>Secondary Target (Panel)</span>
            <span style={{ color: '#FFD200', fontFamily: 'monospace' }}>68.5%</span>
          </div>
          <div style={{ height: '8px', background: '#222', borderRadius: '4px', overflow: 'hidden' }}>
            <div style={{ width: '68.5%', height: '100%', background: '#FFD200' }}></div>
          </div>
        </div>

      </div>
    </div>
  );
}