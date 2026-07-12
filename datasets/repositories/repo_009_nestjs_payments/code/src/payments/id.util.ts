import { randomUUID } from "crypto";

export function generateChargeId(): string {
  return `ch_${randomUUID()}`;
}
