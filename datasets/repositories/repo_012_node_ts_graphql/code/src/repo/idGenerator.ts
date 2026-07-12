export class IdGenerator {
  constructor(private seq: number = 1) {}

  next(): string {
    return String(this.seq++);
  }

  // Snapshot the current sequence so it can be persisted and restored
  // across restarts instead of always starting from 1.
  currentValue(): number {
    return this.seq;
  }

  restore(value: number): void {
    this.seq = value;
  }
}
