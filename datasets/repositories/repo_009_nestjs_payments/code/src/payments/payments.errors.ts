export class ChargeNotFoundError extends Error {
  constructor(chargeId: string) {
    super(`charge not found: ${chargeId}`);
    this.name = "ChargeNotFoundError";
  }
}

export class DuplicateChargeError extends Error {
  constructor(orderId: string) {
    super(`duplicate charge for order: ${orderId}`);
    this.name = "DuplicateChargeError";
  }
}
