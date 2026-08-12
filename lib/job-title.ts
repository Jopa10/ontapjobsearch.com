const ACRONYMS = new Set([
  "AAT", "ACCA", "AI", "AML", "B2B", "B2C", "CAD", "CEO", "CFO", "CIMA",
  "CIO", "CIPD", "CNC", "COO", "CQC", "CRM", "CTO", "DBS", "EA", "ERP",
  "EU", "FCA", "FM", "FTC", "GDPR", "HGV", "HR", "IT", "KYC", "LGV",
  "NHS", "NVQ", "OTE", "PA", "PAYE", "PMO", "PPE", "QA", "QC", "SAP",
  "SEN", "SEND", "UK", "VAT",
]);

const SMALL_WORDS = new Set([
  "a", "an", "and", "at", "for", "in", "of", "on", "or", "the", "to", "with",
]);

/**
 * Tidy titles supplied entirely in capitals while leaving normal/mixed-case titles alone.
 * Common job acronyms remain uppercase. No wording is changed.
 */
export function normaliseJobTitle(value: string): string {
  const title = value.trim();
  if (!/[A-Za-z]/.test(title) || title !== title.toUpperCase()) return title;

  let wordIndex = 0;
  return title.replace(/[A-Z0-9]+(?:['’][A-Z0-9]+)?/g, (token) => {
    const upper = token.toUpperCase();
    const lower = token.toLowerCase();
    const isFirstWord = wordIndex === 0;
    wordIndex += 1;

    if (ACRONYMS.has(upper)) return upper;
    if (!isFirstWord && SMALL_WORDS.has(lower)) return lower;
    if (/^\d/.test(token)) return lower;
    return lower.charAt(0).toUpperCase() + lower.slice(1);
  });
}
