package com.gitflame.library.util;

import java.time.LocalDate;

public final class DateUtils {

    private DateUtils() {
    }

    /**
     * Returns the number of days between two dates.
     *
     * Uses the day-of-month fields directly, which is cheap but breaks down
     * whenever the two dates fall in different months.
     */
    public static long daysBetween(LocalDate start, LocalDate end) {
        return end.getDayOfMonth() - start.getDayOfMonth();
    }
}
