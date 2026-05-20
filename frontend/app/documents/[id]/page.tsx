"use client";

import Link from "next/link";
import { useParams, useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { ErrorMessage } from "@/components/ErrorMessage";
import { OcrResult } from "@/components/OcrResult";
import { StatusBadge } from "@/components/StatusBadge";
import {
  deleteDocument,
  getDocument,
  getOcrResult,
} from "@/lib/api";
import type { DocumentItem, OcrResult as OcrResultType } from "@/lib/api";

export default function DocumentDetailPage() {
  const params = useParams<{ id: string }>();
  const router = useRouter();
  const [token, setToken] = useState<string | null>(null);
  const [document, setDocument] = useState<DocumentItem | null>(null);
  const [ocrResult, setOcrResult] = useState<OcrResultType | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [deleting, setDeleting] = useState(false);

  async function load(currentToken: string) {
    try {
      const nextDocument = await getDocument(currentToken, params.id);
      setDocument(nextDocument);
      setOcrResult(await getOcrResult(currentToken, params.id));
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not load document");
    }
  }

  useEffect(() => {
    const storedToken = localStorage.getItem("access_token");
    if (!storedToken) {
      router.replace("/login");
      return;
    }
    setToken(storedToken);
    load(storedToken);
  }, [params.id, router]);

  useEffect(() => {
    if (!token || !document) {
      return;
    }
    if (document.status === "completed" || document.status === "failed") {
      return;
    }

    const intervalId = window.setInterval(() => {
      load(token);
    }, 2500);

    return () => window.clearInterval(intervalId);
  }, [document, token]);

  async function handleDelete() {
    if (!token || !document) {
      return;
    }
    setDeleting(true);
    try {
      await deleteDocument(token, document.id);
      router.push("/documents");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not delete document");
      setDeleting(false);
    }
  }

  return (
    <main className="shell">
      <header className="topbar">
        <div>
          <Link className="muted" href="/documents">
            Back to documents
          </Link>
          <h1>{document?.original_filename ?? "Document"}</h1>
        </div>
        {document ? (
          <div className="button-row">
            <StatusBadge status={document.status} />
            <button
              className="button danger"
              type="button"
              onClick={handleDelete}
              disabled={deleting}
            >
              {deleting ? "Deleting..." : "Delete"}
            </button>
          </div>
        ) : null}
      </header>

      <ErrorMessage message={error} />

      {document ? (
        <section className="panel">
          <p className="muted">
            {document.content_type} - {(document.size_bytes / 1024).toFixed(1)} KB
          </p>
          {document.error_message ? (
            <ErrorMessage message={document.error_message} />
          ) : null}
          <h2>OCR result</h2>
          <OcrResult text={ocrResult?.ocr_text ?? null} />
        </section>
      ) : null}
    </main>
  );
}
