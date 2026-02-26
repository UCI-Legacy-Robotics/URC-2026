'use client';

export default function GnssWidget() {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
      <h2 style={{ fontSize: '1.2rem', color: '#0064A4', margin: '0 0 1rem 0' }}>Accuracy of GNSS</h2>
      
      <div style={{ flexGrow: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center', gap: '1rem' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', padding: '10px', background: 'rgba(255,255,255,0.05)', borderRadius: '4px' }}>
          <span style={{ color: '#aaa' }}>Latitude:</span>
          <span style={{ fontFamily: 'monospace', color: '#fff' }}>33.6405° N</span>
        </div>
        
        <div style={{ display: 'flex', justifyContent: 'space-between', padding: '10px', background: 'rgba(255,255,255,0.05)', borderRadius: '4px' }}>
          <span style={{ color: '#aaa' }}>Longitude:</span>
          <span style={{ fontFamily: 'monospace', color: '#fff' }}>117.8443° W</span>
        </div>

        <div style={{ display: 'flex', justifyContent: 'space-between', padding: '10px', background: 'rgba(0,100,164,0.1)', border: '1px solid rgba(0,100,164,0.3)', borderRadius: '4px' }}>
          <span style={{ color: '#aaa' }}>Fix Quality:</span>
          <strong style={{ color: '#4ade80' }}>RTK Fixed (2cm)</strong>
        </div>
      </div>
    </div>
  );
}