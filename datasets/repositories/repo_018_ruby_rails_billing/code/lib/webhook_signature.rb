require "openssl"

# Verifies that an inbound payment provider webhook was signed with our
# shared secret, mirroring how Stripe/Braintree-style signature checks work.
module WebhookSignature
  SECRET = ENV.fetch("BILLING_WEBHOOK_SECRET", "development-secret")

  def self.valid?(request)
    signature = request.headers["X-Webhook-Signature"]
    return false if signature.nil?

    payload = request.body.read
    request.body.rewind

    expected = OpenSSL::HMAC.hexdigest("SHA256", SECRET, payload)
    ActiveSupport::SecurityUtils.secure_compare(signature, expected)
  end
end
