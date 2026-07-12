using System.Collections.Generic;
using BookingApi.Models;
using BookingApi.Repositories;
using Microsoft.AspNetCore.Mvc;

namespace BookingApi.Controllers;

[ApiController]
[Route("rooms")]
public class RoomsController : ControllerBase
{
    private readonly RoomRepository _rooms;

    public RoomsController(RoomRepository rooms)
    {
        _rooms = rooms;
    }

    [HttpGet]
    public ActionResult<IReadOnlyList<Room>> GetRooms()
    {
        return Ok(_rooms.GetAll());
    }

    [HttpGet("{id}")]
    public ActionResult<Room> GetRoom(int id)
    {
        var room = _rooms.GetById(id);
        if (room is null)
        {
            return NotFound();
        }

        return Ok(room);
    }
}
