import {
  descriptionBlocks,
  type JobDescriptionBlock,
} from "@/lib/job-description";

type JobDescriptionProps = {
  value: string;
  source: string;
};

const NHS_SOURCE = "nhs jobs";
const NHS_OPEN_BLOCKS = 6;

function DescriptionBlock({
  block,
  index,
}: {
  block: JobDescriptionBlock;
  index: number;
}) {
  if (block.type === "heading") {
    return (
      <h3
        style={{
          fontSize: 17,
          fontWeight: 750,
          margin: index ? "20px 0 8px" : "0 0 8px",
        }}
      >
        {block.text}
      </h3>
    );
  }

  if (block.type === "bullet") {
    return (
      <div style={{ display: "flex", gap: 9, margin: "0 0 8px 4px" }}>
        <span aria-hidden="true">•</span>
        <span>{block.text}</span>
      </div>
    );
  }

  return <p style={{ margin: "0 0 14px" }}>{block.text}</p>;
}

function renderBlocks(blocks: JobDescriptionBlock[], keyPrefix: string) {
  return blocks.map((block, index) => (
    <DescriptionBlock
      key={`${keyPrefix}-${block.type}-${index}`}
      block={block}
      index={index}
    />
  ));
}

export default function JobDescription({ value, source }: JobDescriptionProps) {
  const blocks = descriptionBlocks(value, source);
  const isNhs = source.trim().toLowerCase() === NHS_SOURCE;
  const collapseNhsOverflow = isNhs && blocks.length > NHS_OPEN_BLOCKS;
  const visibleBlocks = collapseNhsOverflow ? blocks.slice(0, NHS_OPEN_BLOCKS) : blocks;
  const overflowBlocks = collapseNhsOverflow ? blocks.slice(NHS_OPEN_BLOCKS) : [];

  return (
    <div style={{ lineHeight: 1.65, color: "#374151", maxWidth: 800 }}>
      {renderBlocks(visibleBlocks, "visible")}

      {overflowBlocks.length ? (
        <details style={{ marginTop: 4 }}>
          <summary
            style={{
              cursor: "pointer",
              color: "#1d4ed8",
              fontWeight: 700,
              marginBottom: 12,
            }}
          >
            Show full NHS role information
          </summary>
          <div style={{ marginTop: 14 }}>
            {renderBlocks(overflowBlocks, "overflow")}
          </div>
        </details>
      ) : null}
    </div>
  );
}
