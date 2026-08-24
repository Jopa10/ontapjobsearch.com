import Link from "next/link";
import styles from "@/components/SectorSwitchBanner.module.css";

type SectorSwitchBannerProps = {
  placement?: "inline" | "overview";
  audience?: "all" | "business";
};

export default function SectorSwitchBanner({
  placement = "inline",
  audience = "all",
}: SectorSwitchBannerProps) {
  const overview = placement === "overview";

  return (
    <aside
      className={`${styles.banner} ${overview ? styles.overview : styles.inline}`}
      data-sector-switch-banner={placement}
      data-sector-banner-view={placement === "inline" ? audience : undefined}
      aria-label="Sector-switching guidance"
    >
      <div>
        <div className={styles.title}>
          {overview
            ? "Public service and charity roles"
            : "Considering public service or charity work?"}
        </div>
        <p className={styles.copy}>
          {overview
            ? "These roles are clearly identified as NHS, school, council, public-service or charity vacancies. Your admin and customer-service skills can often transfer."
            : "Admin and customer-service skills can transfer into NHS, school, council and charity roles—even when the job title looks different."}
        </p>
      </div>
      <Link href="/sector-switching" className={styles.link}>
        How switching sectors works →
      </Link>
    </aside>
  );
}
