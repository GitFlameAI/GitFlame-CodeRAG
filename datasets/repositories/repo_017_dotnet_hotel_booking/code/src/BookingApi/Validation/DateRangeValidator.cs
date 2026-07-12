using System;

namespace BookingApi.Validation;

public class DateRangeValidator
{
    public bool Validate(DateTime checkIn, DateTime checkOut)
    {
        return checkOut >= checkIn;
    }
}
