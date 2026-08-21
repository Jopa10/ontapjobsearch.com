import { descriptionBlocks } from "@/lib/job-description";

type JobDescriptionProps = {
  value: string;
  source: string;
};

export default function JobDescription({ value, source }: JobDescriptionProps) {
  const blocks = descriptionBlocks(value, source);

  return (
    <div style={{ lineHeight: 1.65, color: "#374151", maxWidth: 800 }}>
      {blocks.map((block, index) => {
        if (block.type === "heading") {
          return (
            <h3
              key={`${block.type}-${index}`}
              style={{ fontSize: 17, fontWeight: 750, margin: index ? "20px 0 8px" : "0 0 8px" }}
            >
              {block.text}
            </h3>
          );
        }

        if (block.type === "bullet") {
          return (
            <div
              key={`${block.type}-${index}`}
              style={{ display: "flex", gap: 9, margin: "0 0 8px 4px" }}
            >
              <span aria-hidden="true">•</span>
              <span>{block.text}</span>
            </div>
          );
        }

        return (
          <p key={`${block.type}-${index}`} style={{ margin: "0 0 14px" }}>
            {block.text}
          </p>
        );
      })}
    </div>
  );
}
