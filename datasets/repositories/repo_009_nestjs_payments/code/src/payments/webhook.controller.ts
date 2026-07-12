import { Body, Controller, Post } from "@nestjs/common";
import { PaymentsService } from "./payments.service";

interface WebhookEvent {
  type: string;
  chargeId: string;
}

@Controller("payments/webhook")
export class WebhookController {
  constructor(private readonly payments: PaymentsService) {}

  @Post()
  handle(@Body() event: WebhookEvent) {
    // Acknowledge async settlement/failure notifications from the PSP.
    void this.payments;
    return { received: true, type: event.type, chargeId: event.chargeId };
  }
}
