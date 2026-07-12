interface FilterControlsProps {
  query: string;
  onQueryChange: (query: string) => void;
  sortAscending: boolean;
  onToggleSort: () => void;
}

export function FilterControls({
  query,
  onQueryChange,
  sortAscending,
  onToggleSort,
}: FilterControlsProps) {
  return (
    <div className="filter-controls">
      <input
        type="text"
        placeholder="Filter metrics..."
        value={query}
        onChange={(e) => onQueryChange(e.target.value)}
      />
      <button type="button" onClick={onToggleSort}>
        Sort: {sortAscending ? "Ascending" : "Descending"}
      </button>
    </div>
  );
}
