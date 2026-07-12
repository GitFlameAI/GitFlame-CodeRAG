import { Injectable } from "@nestjs/common";

@Injectable()
export class IdempotencyStore {
  private readonly seen = new Map<string, string>();

  has(key: string): boolean {
    return this.seen.has(key);
  }

  get(key: string): string | undefined {
    return this.seen.get(key);
  }

  remember(key: string, chargeId: string): void {
    this.seen.set(key, chargeId);
  }
}
