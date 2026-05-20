export function OcrResult({ text }: { text: string | null }) {
  return <div className="ocr">{text || "OCR result is not available yet."}</div>;
}
