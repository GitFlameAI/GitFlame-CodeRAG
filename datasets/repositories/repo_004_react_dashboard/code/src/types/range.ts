export type MetricsRange = "7d" | "30d";

export function isMetricsRange(value: string): value is MetricsRange {
  return value === "7d" || value === "30d";
}
