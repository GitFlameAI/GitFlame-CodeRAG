class InvoiceSerializer
  def initialize(invoice)
    @invoice = invoice
  end

  def as_json
    {
      id: @invoice.id,
      subscription_id: @invoice.subscription.id,
      amount: @invoice.amount,
      status: @invoice.status,
      due_at: @invoice.due_at,
      paid_at: @invoice.paid_at
    }
  end
end
