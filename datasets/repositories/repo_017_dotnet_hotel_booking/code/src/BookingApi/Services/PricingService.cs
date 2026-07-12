using System;
using BookingApi.Models;

namespace BookingApi.Services;

public class PricingService
{
    private const decimal WeekendMultiplier = 1.25m;

    public decimal CalculateTotal(Room room, DateTime checkIn, DateTime checkOut)
    {
        var nights = (checkOut - checkIn).Days;
        var total = room.NightlyRate * nights;

        var includesWeekendNight = false;
        for (var date = checkIn; date < checkOut; date = date.AddDays(1))
        {
            if (date.DayOfWeek == DayOfWeek.Saturday || date.DayOfWeek == DayOfWeek.Sunday)
            {
                includesWeekendNight = true;
                break;
            }
        }

        if (includesWeekendNight)
        {
            total *= WeekendMultiplier;
        }

        return total;
    }
}
