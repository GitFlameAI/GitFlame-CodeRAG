const MINOR_UNITS: Record<string, number> = {
  USD: 2,
  EUR: 2,
  JPY: 0,
};

export function toMinorUnits(amount: number, currency = "USD"): number {
  const digits = MINOR_UNITS[currency] ?? 2;
  return Math.round(amount * 10 ** digits);
}

export function formatAmount(amount: number, currency = "USD"): string {
  const digits = MINOR_UNITS[currency] ?? 2;
  return `${(amount / 10 ** digits).toFixed(digits)} ${currency}`;
}
