export interface ChargeDto {
  orderId: string;
  amount: number;
}

export function validateChargeDto(dto: ChargeDto): void {
  if (!dto.orderId) {
    throw new Error("orderId is required");
  }
  if (typeof dto.amount !== "number" || dto.amount <= 0) {
    throw new Error("amount must be a positive number");
  }
}
