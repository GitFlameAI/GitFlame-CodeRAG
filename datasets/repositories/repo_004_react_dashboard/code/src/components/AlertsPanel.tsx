import { Metric } from "../api/client";

interface AlertsPanelProps {
  metrics: Metric[];
  threshold: number;
}

export function AlertsPanel({ metrics, threshold }: AlertsPanelProps) {
  const breached = metrics.filter((metric) => metric.value > threshold);

  if (breached.length === 0) {
    return <p className="alerts-panel alerts-panel--clear">All metrics within range</p>;
  }

  return (
    <ul className="alerts-panel">
      {breached.map((metric) => (
        <li key={metric.name}>
          {metric.name} exceeded threshold ({metric.value} &gt; {threshold})
        </li>
      ))}
    </ul>
  );
}
