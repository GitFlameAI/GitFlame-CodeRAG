class CouponsController < ApplicationController
  def create
    coupon = Coupon.new(
      id: Coupon.all.size + 1,
      code: params[:code],
      percent_off: params[:percent_off],
      expires_at: params[:expires_at]
    )
    render json: { id: coupon.id, code: coupon.code }, status: :created
  end

  def validate
    invoice = Invoice.find(params[:invoice_id])
    return head :not_found unless invoice

    invoice = CouponApplier.new.apply(invoice, params[:code])
    render json: InvoiceSerializer.new(invoice).as_json
  end
end
