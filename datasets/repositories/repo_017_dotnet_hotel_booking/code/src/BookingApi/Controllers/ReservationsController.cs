using BookingApi.DTOs;
using BookingApi.Models;
using BookingApi.Repositories;
using BookingApi.Services;
using BookingApi.Validation;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;

namespace BookingApi.Controllers;

[ApiController]
[Authorize]
[Route("reservations")]
public class ReservationsController : ControllerBase
{
    private readonly ReservationService _reservationService;
    private readonly ReservationRepository _reservations;
    private readonly RoomRepository _rooms;
    private readonly AvailabilityService _availability;
    private readonly PricingService _pricing;
    private readonly DateRangeValidator _dateRangeValidator;

    public ReservationsController(
        ReservationService reservationService,
        ReservationRepository reservations,
        RoomRepository rooms,
        AvailabilityService availability,
        PricingService pricing,
        DateRangeValidator dateRangeValidator)
    {
        _reservationService = reservationService;
        _reservations = reservations;
        _rooms = rooms;
        _availability = availability;
        _pricing = pricing;
        _dateRangeValidator = dateRangeValidator;
    }

    [HttpPost]
    public ActionResult<ReservationResponse> CreateReservation(CreateReservationRequest request)
    {
        if (!_dateRangeValidator.Validate(request.CheckIn, request.CheckOut))
        {
            return BadRequest("Invalid date range.");
        }

        var room = _rooms.GetById(request.RoomId);
        if (room is null)
        {
            return NotFound("Room not found.");
        }

        if (!_availability.IsRoomAvailable(request.RoomId, request.CheckIn, request.CheckOut))
        {
            return Conflict("Room is not available for the requested dates.");
        }

        var reservation = new Reservation
        {
            RoomId = request.RoomId,
            GuestId = request.GuestId,
            CheckIn = request.CheckIn,
            CheckOut = request.CheckOut,
            TotalPrice = _pricing.CalculateTotal(room, request.CheckIn, request.CheckOut)
        };

        var created = _reservationService.Create(reservation);
        return Ok(ToResponse(created));
    }

    [HttpGet("{id}")]
    public ActionResult<ReservationResponse> GetReservation(int id)
    {
        var reservation = _reservations.GetById(id);
        if (reservation is null)
        {
            return NotFound();
        }

        return Ok(ToResponse(reservation));
    }

    private static ReservationResponse ToResponse(Reservation reservation)
    {
        return new ReservationResponse
        {
            Id = reservation.Id,
            RoomId = reservation.RoomId,
            GuestId = reservation.GuestId,
            CheckIn = reservation.CheckIn,
            CheckOut = reservation.CheckOut,
            Status = reservation.Status.ToString(),
            TotalPrice = reservation.TotalPrice
        };
    }
}
