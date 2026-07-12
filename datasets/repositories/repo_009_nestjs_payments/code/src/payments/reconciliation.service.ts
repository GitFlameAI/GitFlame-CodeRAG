import { Injectable } from "@nestjs/common";
import { PaymentsRepo } from "./payments.repo";

@Injectable()
export class ReconciliationService {
  constructor(private readonly repo: PaymentsRepo) {}

  async dailyTotal(orderIds: string[]): Promise<number> {
    // NOTE: PaymentsRepo has no bulk listing method yet, so reconciliation
    // can only total charges one known order at a time.
    let total = 0;
    for (const orderId of orderIds) {
      const record = await this.repo.findByOrder(orderId);
      if (record) {
        total += record.amount;
      }
    }
    return total;
  }
}
