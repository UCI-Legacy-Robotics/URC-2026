'use client';

export default function TelemetryWidget({ label, value, statusColor = '#4ADE80' }) {
  return (
    <div style={{ 
      display: 'flex', 
      flexDirection: 'column', 
      justifyContent: 'center', 
      alignItems: 'center',
      height: '100%',
      padding: '0.5rem'
    }}>
      <h3 style={{ 
        fontSize: '1rem', 
        color: '#A0A0A0', 
        margin: '0 0 0.5rem 0', 
        textTransform: 'uppercase', 
        letterSpacing: '0.5px',
        textAlign: 'center'
      }}>
        {label}
      </h3>
      
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
        {/* Visual status indicator dot */}
        <div style={{ 
          width: '12px', 
          height: '12px', 
          borderRadius: '50%', 
          backgroundColor: statusColor,
          boxShadow: `0 0 8px ${statusColor}`
        }}></div>
        
        <span style={{ 
          fontSize: '1.5rem', 
          fontWeight: 'bold', 
          color: '#FFFFFF',
          fontFamily: 'monospace'
        }}>
          {value}
        </span>
      </div>
    </div>
  );
}