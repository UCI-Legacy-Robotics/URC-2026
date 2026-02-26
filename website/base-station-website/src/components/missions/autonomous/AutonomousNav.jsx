'use client';

import styles from './AutonomousNav.module.css';
import TimerWidget from '@/components/shared/TimerWidget';
import TelemetryWidget from '@/components/shared/TelemetryWidget';
import GnssWidget from '@/components/shared/GnssWidget';
import ConfidenceInterval from '@/components/shared/ConfidenceInterval';
import LedSignal from './subcomponents/LedSignal';

export default function AutonomousNav() {
  return (
    <div className={styles.dashboardGrid}>
      
      {/* Header */}
      <div className={`${styles.card} ${styles.headerCard}`}>
        <h1 className={styles.headerTitle}>Autonomous Navigation Mission</h1>
      </div>

      {/* Left Column */}
      <div className={`${styles.column} ${styles.leftCol}`}>
        <div className={`${styles.card} ${styles.greenAccent}`} style={{ flexGrow: 1 }}>
          <LedSignal />
        </div>

        {/* Note from wireframe: "Important?" -> Styled with warningAccent */}
        <div className={`${styles.card} ${styles.warningAccent}`} style={{ flexGrow: 1.5 }}>
          <ConfidenceInterval />
        </div>

        <div className={`${styles.card} ${styles.blueAccent}`} style={{ flexGrow: 1, padding: '0.5rem' }}>
          <TelemetryWidget label="Distance to Target" value="14.2 m" statusColor="#FFD200" />
        </div>

        <div className={`${styles.card} ${styles.blueAccent}`}>
          <TimerWidget course1="30:00" />
        </div>
      </div>

      {/* Right Column */}
      <div className={`${styles.column} ${styles.rightCol}`}>
        
        {/* Compact Telemetry Row */}
        <div style={{ display: 'flex', gap: '1rem', height: '80px' }}>
          <div className={`${styles.card} ${styles.blueAccent}`} style={{ flex: 1, padding: '0.5rem' }}>
            <TelemetryWidget label="Battery State" value="88%" statusColor="#4ADE80" />
          </div>
          <div className={`${styles.card} ${styles.blueAccent}`} style={{ flex: 1, padding: '0.5rem' }}>
            <TelemetryWidget label="Signal Strength" value="-42 dBm" statusColor="#4ADE80" />
          </div>
        </div>

        <div className={`${styles.card} ${styles.blueAccent}`} style={{ height: '80px', padding: '0.5rem' }}>
          <TelemetryWidget label="Total Distance Travelled" value="2.4 km" statusColor="#0064A4" />
        </div>

        {/* Large Central Camera Area */}
        <div className={`${styles.card} ${styles.greenAccent}`} style={{ flexGrow: 2, padding: 0 }}>
          {/* VideoFeedWidget Placeholder */}
          <div style={{ background: '#000', height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <span style={{ color: '#555' }}>Rover ZED Camera (Auto-Nav Overlay)</span>
          </div>
        </div>

        <div className={`${styles.card} ${styles.blueAccent}`} style={{ flexGrow: 1 }}>
          <GnssWidget />
        </div>
      </div>

    </div>
  );
}