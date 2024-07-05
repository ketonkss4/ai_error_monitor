import ErrorMonitoringChat from "@/components/ErrorMonitoringChat";
import Image from "next/image";


export default function Home() {
  return (
    <main>
      <h1>AI Error Monitoring System</h1>
      <ErrorMonitoringChat />
    </main>
  );
}
