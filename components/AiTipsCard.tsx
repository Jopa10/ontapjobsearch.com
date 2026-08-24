"use client";

import Image from "next/image";
import Link from "next/link";
import styles from "@/components/JobSlicePage.module.css";

type Gtag = (
  command: "event",
  eventName: string,
  parameters: Record<string, string>
) => void;

export default function AiTipsCard() {
  function trackClick() {
    const gtag = (window as Window & { gtag?: Gtag }).gtag;
    gtag?.("event", "ai_tips_click", {
      link_url: "/ai-tips",
      page_path: window.location.pathname,
      placement: "training_sidebar",
    });
  }

  return (
    <section className={styles.aiTipsCard} aria-labelledby="ai-tips-card-title">
      <Image
        src="/assets/ontap-ai-robot-animated.webp"
        alt="Ontap's friendly AI helper waving"
        width={112}
        height={112}
        unoptimized
        className={styles.aiTipsMascot}
      />
      <div className={styles.aiTipsCopy}>
        <div id="ai-tips-card-title" className={styles.aiTipsTitle}>
          Practical AI help
        </div>
        <Link href="/ai-tips" onClick={trackClick} className={styles.aiTipsLink}>
          Explore Ontap&apos;s AI tips →
        </Link>
      </div>
    </section>
  );
}
