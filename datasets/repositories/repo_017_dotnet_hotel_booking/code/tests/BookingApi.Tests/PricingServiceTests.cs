using System;
using BookingApi.Models;
using BookingApi.Services;
using Xunit;

namespace BookingApi.Tests;

public class PricingServiceTests
{
    [Fact]
    public void CalculateTotal_ReturnsBaseRate_ForAllWeekdayStay()
    {
        var service = new PricingService();
        var room = new Room { Id = 1, Number = "101", Type = "Standard", NightlyRate = 100m };

        // Monday 2026-01-05 through Friday 2026-01-09: four weekday nights.
        var total = service.CalculateTotal(room, new DateTime(2026, 1, 5), new DateTime(2026, 1, 9));

        Assert.Equal(400m, total);
    }
}
