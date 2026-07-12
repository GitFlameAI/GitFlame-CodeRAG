# Stand-in for a real payment processor integration (e.g. Stripe).
class PaymentGateway
  ChargeResult = Struct.new(:status, :message)

  def self.charge(amount)
    if amount.to_f.positive? && amount.to_f <= 10_000
      ChargeResult.new("succeeded", "charge approved")
    else
      ChargeResult.new("declined", "charge declined by processor")
    end
  end
end

class BillingService
  def charge(invoice)
    PaymentGateway.charge(invoice.amount)

    invoice.status = "paid"
    invoice.paid_at = Time.current
    invoice
  end

  def generate_invoice(subscription)
    Invoice.new(
      id: Invoice.all.size + 1,
      subscription: subscription,
      amount: subscription.plan.monthly_price,
      due_at: Time.current + 30.days
    )
  end
end
