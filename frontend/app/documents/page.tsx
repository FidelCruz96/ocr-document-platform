"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { DocumentList } from "@/components/DocumentList";
import { DocumentUploader } from "@/components/DocumentUploader";
import { ErrorMessage } from "@/components/ErrorMessage";
import { listDocuments } from "@/lib/api";
import type { DocumentItem } from "@/lib/api";

export default function DocumentsPage() {
  const router = useRouter();
  const [token, setToken] = useState<string | null>(null);
  const [documents, setDocuments] = useState<DocumentItem[]>([]);
  const [error, setError] = useState<string | null>(null);

  async function loadDocuments(currentToken: string) {
    try {
      setError(null);
      setDocuments(await listDocuments(currentToken));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not load documents");
    }
  }

  useEffect(() => {
    const storedToken = localStorage.getItem("access_token");
    if (!storedToken) {
      router.replace("/login");
      return;
    }
    setToken(storedToken);
    loadDocuments(storedToken);
  }, [router]);

  function logout() {
    localStorage.removeItem("access_token");
    router.replace("/login");
  }

  return (
    <main className="shell">
      <header className="topbar">
        <div>
          <h1>Documents</h1>
          <p className="muted">Upload files and review OCR processing status.</p>
        </div>
        <button className="button secondary" type="button" onClick={logout}>
          Sign out
        </button>
      </header>

      <div className="grid">
        {token ? (
          <DocumentUploader
            token={token}
            onUploaded={() => loadDocuments(token)}
          />
        ) : null}

        <section className="panel">
          <h2>Uploaded documents</h2>
          <ErrorMessage message={error} />
          <DocumentList documents={documents} />
        </section>
      </div>
    </main>
  );
}
