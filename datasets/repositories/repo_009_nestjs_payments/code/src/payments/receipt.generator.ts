import { PaymentRecord } from "./payments.repo";

export function generateReceipt(record: PaymentRecord): string {
  return [
    "RECEIPT",
    `Order: ${record.orderId}`,
    `Charge: ${record.chargeId}`,
    `Amount: ${record.amount}`,
  ].join("\n");
}
