const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

export type DocumentStatus = "uploaded" | "processing" | "completed" | "failed";

export type DocumentItem = {
  id: number;
  original_filename: string;
  content_type: string;
  size_bytes: number;
  status: DocumentStatus;
  error_message: string | null;
  created_at: string;
  updated_at: string;
  processed_at: string | null;
};

export type OcrResult = {
  id: number;
  status: DocumentStatus;
  ocr_text: string | null;
  error_message: string | null;
};

async function request<T>(
  path: string,
  options: RequestInit = {},
  token?: string
): Promise<T> {
  const headers = new Headers(options.headers);
  if (token) {
    headers.set("Authorization", `Bearer ${token}`);
  }
  if (options.body && !(options.body instanceof FormData)) {
    headers.set("Content-Type", "application/json");
  }

  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers
  });

  if (!response.ok) {
    const body = await response.json().catch(() => null);
    const message = body?.detail ?? `Request failed with ${response.status}`;
    throw new Error(Array.isArray(message) ? "Invalid request" : message);
  }

  if (response.status === 204) {
    return undefined as T;
  }

  return response.json() as Promise<T>;
}

export async function login(email: string, password: string) {
  return request<{ access_token: string; token_type: string }>("/auth/login", {
    method: "POST",
    body: JSON.stringify({ email, password })
  });
}

export async function listDocuments(token: string) {
  return request<DocumentItem[]>("/documents", {}, token);
}

export async function getDocument(token: string, id: string) {
  return request<DocumentItem>(`/documents/${id}`, {}, token);
}

export async function getOcrResult(token: string, id: string) {
  return request<OcrResult>(`/documents/${id}/ocr`, {}, token);
}

export async function uploadDocument(token: string, file: File) {
  const formData = new FormData();
  formData.append("file", file);
  return request<{ id: number; status: DocumentStatus }>(
    "/documents",
    {
      method: "POST",
      body: formData
    },
    token
  );
}

export async function deleteDocument(token: string, id: number | string) {
  return request<void>(
    `/documents/${id}`,
    {
      method: "DELETE"
    },
    token
  );
}
