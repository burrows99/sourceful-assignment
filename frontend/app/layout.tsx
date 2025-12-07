import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Sourceful - Visual AI for Brand Design",
  description: "AI-powered packaging design and brand visual creation",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="bg-gradient-main min-h-screen antialiased" suppressHydrationWarning>
        {children}
      </body>
    </html>
  );
}
