using System.Collections.Generic;
using System.Linq;
using BookingApi.Data;
using BookingApi.Models;

namespace BookingApi.Repositories;

public class RoomRepository
{
    private readonly BookingDbContext _db;

    public RoomRepository(BookingDbContext db)
    {
        _db = db;
    }

    public Room? GetById(int id)
    {
        _db.Rooms.TryGetValue(id, out var room);
        return room;
    }

    public IReadOnlyList<Room> GetAll()
    {
        return _db.Rooms.Values.ToList();
    }
}
