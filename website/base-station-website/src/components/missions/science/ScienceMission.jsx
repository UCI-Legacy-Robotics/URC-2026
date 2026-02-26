'use client';

import styles from './ScienceMission.module.css';
import TimerWidget from '@/components/shared/TimerWidget';
import TelemetryWidget from '@/components/shared/TelemetryWidget';
import Spectrophotometer from './subcomponents/Spectrophotometer';
import DataCarousel from './subcomponents/DataCarousel';

export default function ScienceMission() {
  return (
    <div className={styles.dashboardGrid}>
      
      {/* Header */}
      <div className={`${styles.card} ${styles.headerCard}`}>
        <h1 className={styles.headerTitle}>Science Mission</h1>
      </div>

      {/* Top Section */}
      <div className={`${styles.card} ${styles.cam360Area} ${styles.blueAccent}`} style={{ padding: 0 }}>
        <div style={{ background: '#000', height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
          <span style={{ color: '#555' }}>360 Camera / Stratographic Feed</span>
        </div>
      </div>

      <div className={`${styles.card} ${styles.timerArea} ${styles.blueAccent}`}>
        <TimerWidget course1="60:00" />
      </div>

      {/* Left Column */}
      <div className={`${styles.column} ${styles.leftCol}`}>
        <div className={`${styles.card} ${styles.blueAccent}`} style={{ flexGrow: 1.2, padding: 0 }}>
          <div style={{ background: '#000', height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <span style={{ color: '#555' }}>Rover FPV</span>
          </div>
        </div>

        <div className={`${styles.card} ${styles.goldAccent}`} style={{ flexGrow: 1 }}>
           <h3 style={{ fontSize: '1.1rem', color: '#A0A0A0', margin: '0 0 10px 0', textTransform: 'uppercase' }}>ArduRover Mini Map</h3>
           <div style={{ flexGrow: 1, background: '#222', display: 'grid', placeItems: 'center', color: '#888', borderRadius: '4px' }}>
             Map Render Area<br/>
             <span style={{fontFamily: 'monospace', color: '#4ade80', marginTop: '5px'}}>33.6405° N, 117.8443° W</span>
           </div>
        </div>

        <div className={`${styles.card} ${styles.blueAccent}`} style={{ flexGrow: 0.8, display: 'flex', flexDirection: 'row', gap: '1rem' }}>
          <div style={{ flex: 1 }}>
            <TelemetryWidget label="Live Power" value="84%" statusColor="#4ADE80" />
          </div>
          <div style={{ width: '1px', background: '#333' }}></div>
          <div style={{ flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center' }}>
            <h3 style={{ fontSize: '0.9rem', color: '#A0A0A0', margin: '0 0 8px 0', textTransform: 'uppercase' }}>Keyboard Ctrl</h3>
            <span style={{ color: '#FFD200', fontFamily: 'monospace', fontSize: '1.2rem', fontWeight: 'bold' }}>ACTIVE</span>
          </div>
        </div>
      </div>

      {/* Right Column */}
      <div className={`${styles.column} ${styles.rightCol}`}>
        <div className={`${styles.card} ${styles.blueAccent}`} style={{ flexGrow: 1.2, padding: 0 }}>
          <div style={{ background: '#000', height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <span style={{ color: '#555' }}>Drill FPV</span>
          </div>
        </div>

        <div className={`${styles.card} ${styles.purpleAccent}`} style={{ flexGrow: 1 }}>
          <Spectrophotometer />
        </div>

        <div className={`${styles.card} ${styles.purpleAccent}`} style={{ flexGrow: 1.5 }}>
          <DataCarousel />
        </div>
      </div>

    </div>
  );
}