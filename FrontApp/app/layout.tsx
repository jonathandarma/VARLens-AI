import "./globals.css";
import type { Metadata } from "next";
export const metadata: Metadata = {title:"VARLens AI",description:"Explainable football decision support"};
export default function Layout({children}:{children:React.ReactNode}) { return <html lang="en"><body>{children}</body></html>; }
