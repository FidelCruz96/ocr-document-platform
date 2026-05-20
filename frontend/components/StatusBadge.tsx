import type { DocumentStatus } from "@/lib/api";

export function StatusBadge({ status }: { status: DocumentStatus }) {
  return <span className={`status ${status}`}>{status}</span>;
}
