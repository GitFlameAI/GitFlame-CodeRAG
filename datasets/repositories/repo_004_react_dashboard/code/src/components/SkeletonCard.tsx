export function SkeletonCard() {
  return (
    <div className="metric-card metric-card--skeleton" aria-hidden="true">
      <span className="skeleton-line skeleton-line--name" />
      <span className="skeleton-line skeleton-line--value" />
    </div>
  );
}
