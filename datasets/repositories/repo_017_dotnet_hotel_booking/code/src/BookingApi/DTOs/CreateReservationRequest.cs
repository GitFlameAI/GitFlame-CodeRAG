using System;

namespace BookingApi.DTOs;

public class CreateReservationRequest
{
    public int RoomId { get; set; }
    public int GuestId { get; set; }
    public DateTime CheckIn { get; set; }
    public DateTime CheckOut { get; set; }
}
