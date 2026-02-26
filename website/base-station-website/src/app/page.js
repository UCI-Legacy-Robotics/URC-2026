'use client';

import { useState } from "react";
import styles from "./page.module.css";
import SideNavbar from "@/components/layout/SideNavbar";
import AutonomousNavWidget from "@/components/missions/autonomous/AutonomousNav";
import DeliveryMissionWidget from "@/components/missions/delivery/DeliveryMission";
import ScienceMissionWidget from "@/components/missions/science/ScienceMission";
import EquipmentServicingWidget from "@/components/missions/servicing/EquipmentServicing";

export default function Home() {
  const [activeMission, setActiveMission] = useState('delivery');

  return (
    <div className={styles.dashboardLayout}>
      <SideNavbar 
        activeMission={activeMission} 
        setActiveMission={setActiveMission} 
      />

      <main className={styles.missionContainer}>
        
        {/* Delivery Mission */}
        <div className={`${styles.missionView} ${activeMission === 'delivery' ? styles.activeView : ''}`}>
          <DeliveryMissionWidget />
        </div>

        {/* Equipment Servicing */}
        <div className={`${styles.missionView} ${activeMission === 'servicing' ? styles.activeView : ''}`}>
          <EquipmentServicingWidget />
        </div>

        {/* Autonomous Navigation */}
        <div className={`${styles.missionView} ${activeMission === 'autonomous' ? styles.activeView : ''}`}>
          <AutonomousNavWidget />
        </div>

        {/* Science Mission */}
        <div className={`${styles.missionView} ${activeMission === 'science' ? styles.activeView : ''}`}>
          <ScienceMissionWidget />
        </div>

      </main>
    </div>
  );
}