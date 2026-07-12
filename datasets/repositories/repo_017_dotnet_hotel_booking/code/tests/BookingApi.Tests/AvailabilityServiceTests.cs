using System;
using BookingApi.Data;
using BookingApi.Models;
using BookingApi.Repositories;
using BookingApi.Services;
using Xunit;

namespace BookingApi.Tests;

public class AvailabilityServiceTests
{
    private static AvailabilityService CreateService(out ReservationRepository reservations)
    {
        var db = new BookingDbContext();
        reservations = new ReservationRepository(db);
        return new AvailabilityService(reservations);
    }

    [Fact]
    public void IsRoomAvailable_ReturnsTrue_WhenRoomHasNoReservations()
    {
        var service = CreateService(out _);

        var available = service.IsRoomAvailable(1, new DateTime(2026, 3, 10), new DateTime(2026, 3, 15));

        Assert.True(available);
    }

    [Fact]
    public void IsRoomAvailable_ReturnsFalse_ForExactDuplicateDateRange()
    {
        var service = CreateService(out var reservations);
        reservations.Add(new Reservation
        {
            RoomId = 1,
            GuestId = 1,
            CheckIn = new DateTime(2026, 3, 10),
            CheckOut = new DateTime(2026, 3, 15),
            Status = ReservationStatus.Confirmed
        });

        var available = service.IsRoomAvailable(1, new DateTime(2026, 3, 10), new DateTime(2026, 3, 15));

        Assert.False(available);
    }
}
