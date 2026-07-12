class SubscriptionSerializer
  def initialize(subscription)
    @subscription = subscription
  end

  def as_json
    {
      id: @subscription.id,
      customer_id: @subscription.customer.id,
      plan_id: @subscription.plan.id,
      status: @subscription.status,
      started_at: @subscription.started_at,
      canceled_at: @subscription.canceled_at
    }
  end
end
