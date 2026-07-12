class WebhooksController < ApplicationController
  def create
    event = JSON.parse(request.body.read)

    case event["type"]
    when "charge.succeeded"
      handle_charge_succeeded(event["data"])
    when "charge.failed"
      handle_charge_failed(event["data"])
    end

    head :ok
  end

  private

  def handle_charge_succeeded(data)
    invoice = Invoice.find(data["invoice_id"])
    BillingService.new.charge(invoice) if invoice
  end

  def handle_charge_failed(data)
    invoice = Invoice.find(data["invoice_id"])
    invoice.status = "failed" if invoice
  end
end
