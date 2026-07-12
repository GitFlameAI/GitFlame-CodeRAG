class SubscriptionsController < ApplicationController
  def create
    customer = Customer.find(params[:customer_id])
    plan = Plan.find(params[:plan_id])
    subscription = SubscriptionService.new.subscribe(customer, plan)
    render json: SubscriptionSerializer.new(subscription).as_json, status: :created
  end

  def cancel
    subscription = Subscription.find(params[:id])
    return head :not_found unless subscription

    SubscriptionService.new.cancel(subscription)
    head :no_content
  end
end
