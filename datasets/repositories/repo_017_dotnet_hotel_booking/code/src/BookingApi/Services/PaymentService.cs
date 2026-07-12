using BookingApi.Data;
using BookingApi.Models;
using BookingApi.Repositories;

namespace BookingApi.Services;

public class PaymentService
{
    private readonly BookingDbContext _db;
    private readonly ReservationRepository _reservations;

    public PaymentService(BookingDbContext db, ReservationRepository reservations)
    {
        _db = db;
        _reservations = reservations;
    }

    public Payment ProcessPayment(Reservation reservation, decimal amount)
    {
        var payment = PaymentGateway.Charge(reservation.Id, amount);
        payment.Id = _db.NextPaymentId();
        _db.Payments[payment.Id] = payment;

        reservation.Status = ReservationStatus.Confirmed;
        _reservations.Update(reservation);

        return payment;
    }
}

internal static class PaymentGateway
{
    // Declines charges above 5000 to mimic a card issuer's fraud threshold.
    public static Payment Charge(int reservationId, decimal amount)
    {
        var status = amount <= 5000m ? PaymentStatus.Succeeded : PaymentStatus.Declined;
        return new Payment
        {
            ReservationId = reservationId,
            Amount = amount,
            Status = status
        };
    }
}
