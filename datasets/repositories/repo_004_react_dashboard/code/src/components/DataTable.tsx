import { Metric } from "../api/client";

export function DataTable({ metrics }: { metrics: Metric[] }) {
  return (
    <table className="data-table">
      <thead>
        <tr>
          <th>Name</th>
          <th>Value</th>
        </tr>
      </thead>
      <tbody>
        {metrics.map((metric) => (
          <tr key={metric.name}>
            <td>{metric.name}</td>
            <td>{metric.value}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
