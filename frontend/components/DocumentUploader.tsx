"use client";

import { FormEvent, useRef, useState } from "react";
import { uploadDocument } from "@/lib/api";
import { ErrorMessage } from "./ErrorMessage";

export function DocumentUploader({
  token,
  onUploaded
}: {
  token: string;
  onUploaded: () => void;
}) {
  const formRef = useRef<HTMLFormElement | null>(null);
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!file) {
      setError("Select a document first.");
      return;
    }

    setLoading(true);
    setError(null);
    try {
      await uploadDocument(token, file);
      setFile(null);
      formRef.current?.reset();
      onUploaded();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Upload failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="panel">
      <h2>Upload document</h2>
      <form className="form" onSubmit={handleSubmit} ref={formRef}>
        <label className="field">
          <span>JPG, PNG or PDF up to 10 MB</span>
          <input
            type="file"
            accept=".jpg,.jpeg,.png,.pdf,image/jpeg,image/png,application/pdf"
            onChange={(event) => setFile(event.target.files?.[0] ?? null)}
          />
        </label>
        <ErrorMessage message={error} />
        <button className="button" type="submit" disabled={loading}>
          {loading ? "Uploading..." : "Upload"}
        </button>
      </form>
    </section>
  );
}
