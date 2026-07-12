# Lightweight mailer stub. Returns the message as a plain hash instead of
# rendering ActionMailer views, since outbound email is mocked in tests.
class BillingMailer
  def self.payment_failed_email(invoice)
    {
      to: invoice.subscription.customer.email,
      subject: "We couldn't process your payment",
      body: "Your payment of #{invoice.amount} for invoice ##{invoice.id} failed."
    }
  end

  def self.invoice_paid_email(invoice)
    {
      to: invoice.subscription.customer.email,
      subject: "Payment received",
      body: "Thanks! We received your payment of #{invoice.amount} for invoice ##{invoice.id}."
    }
  end
end
