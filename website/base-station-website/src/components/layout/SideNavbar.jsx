import Image from 'next/image';
import styles from './SideNavbar.module.css';

export default function SideNavbar({ activeMission, setActiveMission }) {
  const navItems = [
    { id: 'delivery', label: 'Delivery Mission' },
    { id: 'servicing', label: 'Equipment Servicing' },
    { id: 'autonomous', label: 'Autonomous Navigation' },
    { id: 'science', label: 'Science Mission' },
  ];

  return (
    <nav className={styles.sidebar}>
      <div className={styles.logoContainer}>
        {/* Assumes your logo is in public/logo.png */}
        <Image 
          src="/logo.png" 
          alt="Legacy Robotics Logo" 
          width={90} 
          height={90} 
          className={styles.logo}
        />
        <h2 className={styles.title}>Legacy Robotics</h2>
        <p className={styles.subtitle}>Mission Control</p>
      </div>

      <ul className={styles.navList}>
        {navItems.map((item) => (
          <li key={item.id} className={styles.navItem}>
            <button
              className={`${styles.navButton} ${
                activeMission === item.id ? styles.active : ''
              }`}
              onClick={() => setActiveMission(item.id)}
            >
              {item.label}
            </button>
          </li>
        ))}
      </ul>
    </nav>
  );
}