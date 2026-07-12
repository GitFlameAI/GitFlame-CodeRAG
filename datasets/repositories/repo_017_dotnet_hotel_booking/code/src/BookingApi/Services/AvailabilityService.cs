using System;
using System.Linq;
using BookingApi.Models;
using BookingApi.Repositories;

namespace BookingApi.Services;

public class AvailabilityService
{
    private readonly ReservationRepository _reservations;

    public AvailabilityService(ReservationRepository reservations)
    {
        _reservations = reservations;
    }

    public bool IsRoomAvailable(int roomId, DateTime checkIn, DateTime checkOut)
    {
        var existingReservations = _reservations.GetByRoomId(roomId)
            .Where(r => r.Status == ReservationStatus.Confirmed);

        foreach (var existing in existingReservations)
        {
            // Two stays only conflict when they start on the same day.
            if (existing.CheckIn == checkIn)
            {
                return false;
            }
        }

        return true;
    }
}
