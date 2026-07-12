export type PaymentMethodType = "card" | "bank_transfer" | "wallet";

export interface PaymentMethod {
  id: string;
  type: PaymentMethodType;
  last4?: string;
  customerId: string;
}

export function maskPaymentMethod(method: PaymentMethod): string {
  return method.last4 ? `${method.type} ending in ${method.last4}` : method.type;
}
