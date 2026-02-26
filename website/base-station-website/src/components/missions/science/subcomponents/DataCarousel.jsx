'use client';

export default function DataCarousel() {
  return (
    <div style={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '10px' }}>
        <h3 style={{ fontSize: '1.1rem', color: '#A0A0A0', margin: 0, textTransform: 'uppercase' }}>Science Data Analysis</h3>
        {/* Carousel Indicators */}
        <div style={{ display: 'flex', gap: '6px' }}>
          <div style={{ width: '8px', height: '8px', borderRadius: '50%', background: '#c084fc' }}></div>
          <div style={{ width: '8px', height: '8px', borderRadius: '50%', background: '#444' }}></div>
          <div style={{ width: '8px', height: '8px', borderRadius: '50%', background: '#444' }}></div>
        </div>
      </div>
      
      <div style={{ flexGrow: 1, background: '#222', borderRadius: '6px', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', border: '1px solid #333' }}>
        <span style={{ color: '#888', marginBottom: '10px' }}>Graph Segment 1: Soil Composition</span>
        {/* Placeholder for Chart.js or Recharts */}
        <div style={{ width: '80%', height: '60%', borderBottom: '2px solid #555', borderLeft: '2px solid #555', position: 'relative' }}>
          <div style={{ position: 'absolute', bottom: '10%', left: '10%', width: '20%', height: '40%', background: '#c084fc' }}></div>
          <div style={{ position: 'absolute', bottom: '10%', left: '40%', width: '20%', height: '70%', background: '#0064A4' }}></div>
          <div style={{ position: 'absolute', bottom: '10%', left: '70%', width: '20%', height: '30%', background: '#FFD200' }}></div>
        </div>
      </div>
    </div>
  );
}