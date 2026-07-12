export function roundToPrecision(value: number, digits: number): number {
  const factor = 10 ** digits;
  return Math.round(value * factor) / factor;
}

export function isBelowThreshold(value: number, threshold: number): boolean {
  return Math.abs(value) < threshold;
}
