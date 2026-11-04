import type { ReactNode } from "react";

export const metadata = { title: "Course Module Builder" };

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body style={{ fontFamily: "system-ui, sans-serif", margin: 0, padding: 16, maxWidth: 720 }}>
        {children}
      </body>
    </html>
  );
}
