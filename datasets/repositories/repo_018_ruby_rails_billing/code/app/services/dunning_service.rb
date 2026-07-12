class DunningService
  def initialize(billing_service: BillingService.new)
    @billing_service = billing_service
  end

  def retry_failed_invoices
    invoices_to_retry = Invoice.all.select { |invoice| invoice.due_at && invoice.due_at <= Time.current }

    invoices_to_retry.each do |invoice|
      @billing_service.charge(invoice)
    end
  end
end
