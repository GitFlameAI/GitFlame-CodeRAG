class ChargeInvoiceJob < ApplicationJob
  queue_as :billing

  def perform(invoice_id)
    invoice = Invoice.find(invoice_id)
    return unless invoice

    BillingService.new.charge(invoice)
  end
end
