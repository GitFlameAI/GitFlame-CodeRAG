import { Injectable } from "@nestjs/common";

@Injectable()
export class FraudCheckService {
  private readonly HIGH_RISK_THRESHOLD = 100_000;

  assessRisk(amount: number): "low" | "medium" | "high" {
    if (amount >= this.HIGH_RISK_THRESHOLD) {
      return "high";
    }
    if (amount >= this.HIGH_RISK_THRESHOLD / 10) {
      return "medium";
    }
    return "low";
  }
}
