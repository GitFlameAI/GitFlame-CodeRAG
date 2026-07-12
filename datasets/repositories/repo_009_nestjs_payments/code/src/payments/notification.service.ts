import { Injectable } from "@nestjs/common";

@Injectable()
export class NotificationService {
  private readonly sent: string[] = [];

  async notifyChargeSucceeded(orderId: string, chargeId: string): Promise<void> {
    this.sent.push(`Charge ${chargeId} succeeded for order ${orderId}`);
  }

  getSentNotifications(): string[] {
    return [...this.sent];
  }
}
