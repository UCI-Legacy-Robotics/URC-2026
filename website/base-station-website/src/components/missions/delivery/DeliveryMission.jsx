'use client';

import styles from './DeliveryMission.module.css';
import TimerWidget from '@/components/shared/TimerWidget';
import GnssWidget from '@/components/shared/GnssWidget';
import TaskList from './subcomponents/TaskList';
import TelemetryWidget from '@/components/shared/TelemetryWidget';

export default function DeliveryMission() {
  return (
    <div className={styles.dashboardGrid}>
      
      {/* Header */}
      <div className={`${styles.card} ${styles.headerCard}`}>
        <h1 className={styles.headerTitle}>Delivery Mission</h1>
      </div>

      {/* Top Left: Timers */}
      <div className={`${styles.card} ${styles.timerArea}`}>
        <TimerWidget course1="12:45" course2="15:00" />
      </div>

      {/* Bottom Left: Points */}
      <div className={`${styles.card} ${styles.pointsArea}`}>
        <h3 style={{ color: '#aaa', margin: '0 0 10px 0' }}>Points</h3>
        <p>Course 1: <strong>45 pts</strong></p>
        <p>Course 2: <strong>Pending</strong></p>
      </div>

      {/* Middle: GNSS Accuracy */}
      <div className={`${styles.card} ${styles.gnssArea}`}>
        <GnssWidget />
      </div>

      {/* Bottom Spanning Left/Mid: Tasks */}
      <div className={`${styles.card} ${styles.tasksArea}`}>
        <TaskList />
      </div>

      {/* Right Column: Telemetry, Signals, Camera, and Map */}
      <div className={styles.rightCol}>
        <div className={`${styles.card} ${styles.telemetryCard}`}>
          <TelemetryWidget label="Power Remaining" value="87%" />
        </div>
        
        <div className={`${styles.card} ${styles.telemetryCard}`}>
          <p>Rover Signal: <span style={{color: '#4ade80'}}>Y</span></p>
          <p>Drone Signal: <span style={{color: '#4ade80'}}>Y</span></p>
        </div>

        <div className={`${styles.card} ${styles.telemetryCard}`} style={{ flexGrow: 1 }}>
          <h3 style={{ margin: '0 0 10px 0', fontSize: '1rem' }}>Object In View</h3>
          {/* Placeholder for VideoFeedWidget */}
          <div style={{ background: '#000', height: '100%', borderRadius: '4px', display: 'grid', placeItems: 'center' }}>
            <span style={{ color: '#555' }}>Camera Feed Standby</span>
          </div>
        </div>

        <div className={styles.card} style={{ flexGrow: 1, padding: 0, overflow: 'hidden' }}>
          {/* Map Image Placeholder */}
          <div style={{ background: '#fff', height: '100%', display: 'grid', placeItems: 'center', color: '#000' }}>
            <span>Map Render Area</span>
          </div>
        </div>
      </div>

    </div>
  );
}