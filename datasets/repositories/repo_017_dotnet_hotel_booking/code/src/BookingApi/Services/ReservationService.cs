using System.Collections.Generic;
using System.Linq;
using BookingApi.Models;
using BookingApi.Repositories;

namespace BookingApi.Services;

public class ReservationService
{
    private readonly ReservationRepository _reservations;
    private readonly HashSet<int> _hiddenFromGuestHistory = new();

    public ReservationService(ReservationRepository reservations)
    {
        _reservations = reservations;
    }

    public Reservation Create(Reservation reservation)
    {
        reservation.Status = ReservationStatus.Confirmed;
        return _reservations.Add(reservation);
    }

    public IReadOnlyList<Reservation> GetReservationsForGuest(int guestId)
    {
        return _reservations.GetByGuestId(guestId)
            .Where(r => !_hiddenFromGuestHistory.Contains(r.Id))
            .ToList();
    }

    public bool CancelReservation(int id)
    {
        var reservation = _reservations.GetById(id);
        if (reservation is null)
        {
            return false;
        }

        // Removed from the guest's booking history immediately.
        _hiddenFromGuestHistory.Add(reservation.Id);
        return true;
    }
}
