using BookingApi.Repositories;
using BookingApi.Services;
using Microsoft.AspNetCore.Mvc;

namespace BookingApi.Controllers;

[ApiController]
[Route("payments")]
public class PaymentsController : ControllerBase
{
    private readonly PaymentService _paymentService;
    private readonly ReservationRepository _reservations;

    public PaymentsController(PaymentService paymentService, ReservationRepository reservations)
    {
        _paymentService = paymentService;
        _reservations = reservations;
    }

    [HttpPost]
    public ActionResult<PaymentResponse> CreatePayment(CreatePaymentRequest request)
    {
        var reservation = _reservations.GetById(request.ReservationId);
        if (reservation is null)
        {
            return NotFound("Reservation not found.");
        }

        var payment = _paymentService.ProcessPayment(reservation, request.Amount);

        return Ok(new PaymentResponse
        {
            PaymentId = payment.Id,
            ReservationId = payment.ReservationId,
            Status = payment.Status.ToString()
        });
    }
}

public class CreatePaymentRequest
{
    public int ReservationId { get; set; }
    public decimal Amount { get; set; }
}

public class PaymentResponse
{
    public int PaymentId { get; set; }
    public int ReservationId { get; set; }
    public string Status { get; set; } = string.Empty;
}
