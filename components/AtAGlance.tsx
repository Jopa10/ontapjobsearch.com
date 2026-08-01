import styles from "@/components/AtAGlance.module.css";

type AtAGlanceProps = {
  attributes: string[];
  variant?: "card" | "detail";
};

export default function AtAGlance({
  attributes,
  variant = "card",
}: AtAGlanceProps) {
  if (attributes.length < 2) return null;

  return (
    <div
      className={`${styles.atAGlance} ${
        variant === "detail" ? styles.detail : ""
      }`}
    >
      <span className={styles.label}>At a glance:</span>{" "}
      <span className={styles.attributes}>{attributes.join(" • ")}</span>
    </div>
  );
}
