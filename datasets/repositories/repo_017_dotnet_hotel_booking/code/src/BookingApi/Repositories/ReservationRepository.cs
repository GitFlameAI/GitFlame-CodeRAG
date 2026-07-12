using System.Collections.Generic;
using System.Linq;
using BookingApi.Data;
using BookingApi.Models;

namespace BookingApi.Repositories;

public class ReservationRepository
{
    private readonly BookingDbContext _db;

    public ReservationRepository(BookingDbContext db)
    {
        _db = db;
    }

    public Reservation Add(Reservation reservation)
    {
        reservation.Id = _db.NextReservationId();
        _db.Reservations[reservation.Id] = reservation;
        return reservation;
    }

    public Reservation? GetById(int id)
    {
        _db.Reservations.TryGetValue(id, out var reservation);
        return reservation;
    }

    public IReadOnlyList<Reservation> GetByRoomId(int roomId)
    {
        return _db.Reservations.Values.Where(r => r.RoomId == roomId).ToList();
    }

    public IReadOnlyList<Reservation> GetByGuestId(int guestId)
    {
        return _db.Reservations.Values.Where(r => r.GuestId == guestId).ToList();
    }

    public void Update(Reservation reservation)
    {
        _db.Reservations[reservation.Id] = reservation;
    }
}
