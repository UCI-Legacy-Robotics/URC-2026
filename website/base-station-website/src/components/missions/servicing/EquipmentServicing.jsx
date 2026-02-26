'use client';

import styles from './EquipmentServicing.module.css';
import TimerWidget from '@/components/shared/TimerWidget';
import TelemetryWidget from '@/components/shared/TelemetryWidget';
import GnssWidget from '@/components/shared/GnssWidget';
import TaskStatuses from './subcomponents/TaskStatuses';
import DigitalKeyboardStatus from './subcomponents/DigitalKeyboardStatus';
import ConfidenceInterval from '../../shared/ConfidenceInterval';

export default function EquipmentServicing() {
  return (
    <div className={styles.dashboardGrid}>
      
      {/* Header */}
      <div className={`${styles.card} ${styles.headerCard}`}>
        <h1 className={styles.headerTitle}>Equipment Servicing Mission</h1>
      </div>

      {/* Left Column */}
      <div className={`${styles.column} ${styles.leftCol}`}>
        <div className={`${styles.card} ${styles.blueAccent}`} style={{ flexGrow: 1.5, padding: 0 }}>
          {/* VideoFeedWidget Placeholder */}
          <div style={{ background: '#000', height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <span style={{ color: '#555' }}>Rover ZED Camera Feed</span>
          </div>
        </div>

        <div className={`${styles.card} ${styles.goldAccent}`} style={{ flexGrow: 1 }}>
          <TaskStatuses />
        </div>

        <div className={`${styles.card} ${styles.greenAccent}`} style={{ flexGrow: 1 }}>
          <DigitalKeyboardStatus />
        </div>

        <div className={`${styles.card} ${styles.blueAccent}`}>
          <TimerWidget course1="45:00" />
        </div>
      </div>

      {/* Right Column */}
      <div className={`${styles.column} ${styles.rightCol}`}>
        
        {/* Compact Telemetry Row */}
        <div style={{ display: 'flex', gap: '1rem', height: '80px' }}>
          <div className={`${styles.card} ${styles.blueAccent}`} style={{ flex: 1, padding: '0.5rem' }}>
            <TelemetryWidget label="Rover Battery" value="92%" statusColor="#4ADE80" />
          </div>
          <div className={`${styles.card} ${styles.blueAccent}`} style={{ flex: 1, padding: '0.5rem' }}>
            <TelemetryWidget label="Signal" value="-45 dBm" statusColor="#4ADE80" />
          </div>
        </div>

        <div className={`${styles.card} ${styles.blueAccent}`} style={{ height: '80px', padding: '0.5rem' }}>
          <TelemetryWidget label="Total Distance" value="1.2 km" statusColor="#FFD200" />
        </div>

        <div className={`${styles.card} ${styles.goldAccent}`} style={{ flexGrow: 1.5 }}>
          <ConfidenceInterval />
        </div>

        <div className={`${styles.card} ${styles.blueAccent}`} style={{ flexGrow: 1 }}>
          <GnssWidget />
        </div>
      </div>

      {/* Footer / Autonomous Mode Status */}
      <div className={`${styles.card} ${styles.footerCard}`}>
        <h2 style={{ fontSize: '1.2rem', color: '#A0A0A0', margin: '0 1rem 0 0', textTransform: 'uppercase' }}>
          Autonomous Mode Status:
        </h2>
        <span style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#4ade80', fontFamily: 'monospace', letterSpacing: '1px' }}>
          STANDBY / READY
        </span>
      </div>

    </div>
  );
}