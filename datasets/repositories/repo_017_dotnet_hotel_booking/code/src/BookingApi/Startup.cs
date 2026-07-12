using BookingApi.Data;
using BookingApi.Middleware;
using BookingApi.Repositories;
using BookingApi.Services;
using BookingApi.Validation;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;

namespace BookingApi;

public class Startup
{
    public void ConfigureServices(IServiceCollection services)
    {
        services.AddControllers();
        services.AddAuthorization();

        services.AddSingleton<BookingDbContext>();
        services.AddSingleton<RoomRepository>();
        services.AddSingleton<ReservationRepository>();

        services.AddSingleton<AvailabilityService>();
        services.AddSingleton<PricingService>();
        services.AddSingleton<ReservationService>();
        services.AddSingleton<PaymentService>();
        services.AddSingleton<DateRangeValidator>();
    }

    public void Configure(IApplicationBuilder app, IWebHostEnvironment env)
    {
        app.UseMiddleware<ExceptionMiddleware>();

        app.UseRouting();
        app.UseAuthorization();

        app.UseEndpoints(endpoints =>
        {
            endpoints.MapControllers();
        });
    }
}
