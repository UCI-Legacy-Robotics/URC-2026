'use client';

export default function Spectrophotometer() {
  return (
    <div style={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      <h3 style={{ fontSize: '1.1rem', color: '#A0A0A0', margin: '0 0 10px 0', textTransform: 'uppercase' }}>Spectrophotometer Readings</h3>
      <div style={{ flexGrow: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center', gap: '10px' }}>
        
        <div style={{ display: 'flex', justifyContent: 'space-between', padding: '8px 12px', background: 'rgba(192, 132, 252, 0.1)', borderRadius: '4px' }}>
          <span style={{ color: '#E0E0E0' }}>Absorbance (450nm)</span>
          <span style={{ fontFamily: 'monospace', color: '#c084fc', fontWeight: 'bold' }}>0.842 A</span>
        </div>

        <div style={{ display: 'flex', justifyContent: 'space-between', padding: '8px 12px', background: 'rgba(192, 132, 252, 0.1)', borderRadius: '4px' }}>
          <span style={{ color: '#E0E0E0' }}>Transmittance</span>
          <span style={{ fontFamily: 'monospace', color: '#c084fc', fontWeight: 'bold' }}>14.3 %</span>
        </div>

        <div style={{ display: 'flex', justifyContent: 'space-between', padding: '8px 12px', background: 'rgba(192, 132, 252, 0.1)', borderRadius: '4px' }}>
          <span style={{ color: '#E0E0E0' }}>Concentration Est.</span>
          <span style={{ fontFamily: 'monospace', color: '#c084fc', fontWeight: 'bold' }}>2.1 mg/L</span>
        </div>

      </div>
    </div>
  );
}