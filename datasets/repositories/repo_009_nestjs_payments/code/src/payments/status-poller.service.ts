import { Injectable } from "@nestjs/common";

export type PaymentStatus = "pending" | "settled" | "failed";

@Injectable()
export class StatusPollerService {
  private readonly statuses = new Map<string, PaymentStatus>();

  markPending(chargeId: string): void {
    this.statuses.set(chargeId, "pending");
  }

  markSettled(chargeId: string): void {
    this.statuses.set(chargeId, "settled");
  }

  getStatus(chargeId: string): PaymentStatus {
    return this.statuses.get(chargeId) ?? "pending";
  }
}
