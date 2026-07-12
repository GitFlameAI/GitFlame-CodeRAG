export type Range = "7d" | "30d";

interface RangeSelectorProps {
  value: Range;
  onChange: (range: Range) => void;
}

export function RangeSelector({ value, onChange }: RangeSelectorProps) {
  return (
    <select value={value} onChange={(e) => onChange(e.target.value as Range)}>
      <option value="7d">7 days</option>
      <option value="30d">30 days</option>
    </select>
  );
}
