import { Metric } from "../api/client";

export function metricsToCsv(metrics: Metric[]): string {
  const header = "name,value";
  const rows = metrics.map((metric) => `${metric.name},${metric.value}`);
  return [header, ...rows].join("\n");
}

export function downloadCsv(filename: string, csv: string): void {
  const blob = new Blob([csv], { type: "text/csv" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = filename;
  link.click();
  URL.revokeObjectURL(url);
}
