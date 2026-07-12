class CouponApplier
  def apply(invoice, coupon_code)
    coupon = Coupon.find_by_code(coupon_code)
    return invoice unless coupon

    discount = invoice.amount * (coupon.percent_off / 100.0)
    invoice.amount = (invoice.amount - discount).round(2)
    invoice
  end
end
