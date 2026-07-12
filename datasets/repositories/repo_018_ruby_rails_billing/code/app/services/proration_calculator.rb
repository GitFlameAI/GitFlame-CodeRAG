class ProrationCalculator
  DAYS_IN_MONTH = 30

  # Prorates the plan's monthly price for the days remaining in the
  # current billing period, e.g. when a customer upgrades mid-cycle.
  def calculate(plan, days_remaining)
    daily_rate = plan.monthly_price / DAYS_IN_MONTH.to_f
    (daily_rate * days_remaining).round(2)
  end
end
