import Link from "next/link";
import { StatusBadge } from "./StatusBadge";
import type { DocumentItem } from "@/lib/api";

export function DocumentList({ documents }: { documents: DocumentItem[] }) {
  if (documents.length === 0) {
    return <p className="muted">No documents uploaded yet.</p>;
  }

  return (
    <div className="document-list">
      {documents.map((document) => (
        <Link
          className="document-row"
          href={`/documents/${document.id}`}
          key={document.id}
        >
          <div>
            <p className="document-title">{document.original_filename}</p>
            <span className="muted">
              {(document.size_bytes / 1024).toFixed(1)} KB
            </span>
          </div>
          <StatusBadge status={document.status} />
        </Link>
      ))}
    </div>
  );
}
