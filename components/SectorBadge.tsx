import type { JobSectorLabel } from "@/lib/job-sector";
import styles from "@/components/SectorBadge.module.css";

export default function SectorBadge({ label }: { label: JobSectorLabel }) {
  return <span className={styles.badge}>{label}</span>;
}
