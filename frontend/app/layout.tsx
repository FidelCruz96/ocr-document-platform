import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "OCR Document Platform",
  description: "Upload documents and review mock OCR results"
};

export default function RootLayout({
  children
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
