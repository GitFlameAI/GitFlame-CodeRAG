using BookingApi.Models;

namespace BookingApi.Data;

/// <summary>
/// Lightweight in-memory store standing in for a real EF Core DbContext.
/// </summary>
public class BookingDbContext
{
    public Dictionary<int, Room> Rooms { get; } = new();
    public Dictionary<int, Guest> Guests { get; } = new();
    public Dictionary<int, Reservation> Reservations { get; } = new();
    public Dictionary<int, Payment> Payments { get; } = new();

    private int _nextReservationId = 1;
    private int _nextPaymentId = 1;

    public BookingDbContext()
    {
        Rooms[1] = new Room { Id = 1, Number = "101", Type = "Standard", NightlyRate = 90m };
        Rooms[2] = new Room { Id = 2, Number = "102", Type = "Deluxe", NightlyRate = 150m };
        Rooms[3] = new Room { Id = 3, Number = "201", Type = "Suite", NightlyRate = 260m };

        Guests[1] = new Guest { Id = 1, Name = "Alice Nowak", Email = "alice@example.com" };
        Guests[2] = new Guest { Id = 2, Name = "Ben Carter", Email = "ben@example.com" };
    }

    public int NextReservationId() => _nextReservationId++;

    public int NextPaymentId() => _nextPaymentId++;
}
