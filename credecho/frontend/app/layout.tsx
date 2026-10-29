import "./globals.css";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "CredEcho — MSME Financial Health Card",
  description: "AI/ML alternate-data credit scoring for NTC/NTB MSMEs",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="font-sans min-h-screen">{children}</body>
    </html>
  );
}
