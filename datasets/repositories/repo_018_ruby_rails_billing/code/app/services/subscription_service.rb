class SubscriptionService
  def subscribe(customer, plan)
    subscription = Subscription.new(id: next_id, customer: customer, plan: plan)
    customer.active_subscriptions << subscription
    subscription
  end

  def cancel(subscription)
    customer = subscription.customer
    customer.active_subscriptions.delete(subscription)
    subscription
  end

  private

  def next_id
    Subscription.all.size + 1
  end
end
