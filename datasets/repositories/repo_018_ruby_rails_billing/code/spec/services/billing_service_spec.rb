require "rails_helper"

RSpec.describe BillingService do
  describe "#charge" do
    it "marks the invoice as paid when the gateway approves the charge" do
      customer = Customer.new(id: 1, name: "Ada Lovelace", email: "ada@example.com")
      plan = Plan.new(id: 1, name: "Pro", monthly_price: 49.0)
      subscription = Subscription.new(id: 1, customer: customer, plan: plan)
      invoice = Invoice.new(id: 1, subscription: subscription, amount: 49.0)

      BillingService.new.charge(invoice)

      expect(invoice.status).to eq("paid")
      expect(invoice.paid_at).not_to be_nil
    end
  end
end
