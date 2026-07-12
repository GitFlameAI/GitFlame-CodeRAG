require "rails_helper"

RSpec.describe ProrationCalculator do
  describe "#calculate" do
    it "prorates a 30-day month based on days remaining" do
      plan = Plan.new(id: 1, name: "Pro", monthly_price: 300.0)

      amount = ProrationCalculator.new.calculate(plan, 15)

      expect(amount).to eq(150.0)
    end

    it "returns zero when no days remain in the billing period" do
      plan = Plan.new(id: 2, name: "Starter", monthly_price: 90.0)

      amount = ProrationCalculator.new.calculate(plan, 0)

      expect(amount).to eq(0.0)
    end
  end
end
