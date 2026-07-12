class InvoicesController < ApplicationController
  def index
    customer = Customer.find(params[:customer_id])
    invoices = Invoice.all.select { |invoice| invoice.subscription.customer == customer }
    render json: invoices.map { |invoice| InvoiceSerializer.new(invoice).as_json }
  end

  def show
    invoice = Invoice.find(params[:id])
    return head :not_found unless invoice

    render json: InvoiceSerializer.new(invoice).as_json
  end
end
