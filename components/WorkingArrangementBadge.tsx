type WorkingArrangementBadgeProps = {
  workingArrangement?: string;
  workingArrangementText?: string;
};

const QUALIFYING_ARRANGEMENTS = new Set(["hybrid", "partly_remote"]);

export default function WorkingArrangementBadge({
  workingArrangement,
  workingArrangementText,
}: WorkingArrangementBadgeProps) {
  if (!workingArrangement || !QUALIFYING_ARRANGEMENTS.has(workingArrangement)) {
    return null;
  }

  const detail = (workingArrangementText || "").trim();
  const showDetail = detail && detail.toLocaleLowerCase("en-GB") !== "hybrid working";

  return (
    <span
      style={{
        display: "inline-flex",
        alignItems: "center",
        flexWrap: "wrap",
        gap: 6,
        marginLeft: 6,
      }}
    >
      <span
        data-working-arrangement-badge="hybrid"
        style={{
          display: "inline-block",
          padding: "2px 7px",
          fontSize: 11,
          fontWeight: 700,
          lineHeight: 1.4,
          borderRadius: 6,
          background: "#ecfdf5",
          color: "#047857",
          border: "1px solid #a7f3d0",
          whiteSpace: "nowrap",
        }}
      >
        Hybrid working
      </span>
      {showDetail ? (
        <span
          data-working-arrangement-detail="true"
          style={{ fontSize: 12, color: "#4b5563", whiteSpace: "nowrap" }}
        >
          {detail}
        </span>
      ) : null}
    </span>
  );
}
