package com.gitflame.library.service;

import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.time.temporal.ChronoUnit;

import static com.gitflame.library.config.AppConfig.LATE_FEE_PER_DAY;
import static com.gitflame.library.config.AppConfig.MAX_LATE_FEE;

@Service
public class FeeCalculator {

    /** Computes the late fee owed for a loan, capped at {@link com.gitflame.library.config.AppConfig#MAX_LATE_FEE}. */
    public double calculateLateFee(LocalDateTime dueAt, LocalDateTime returnedAt) {
        if (returnedAt.isBefore(dueAt)) {
            return 0.0;
        }

        long daysLate = ChronoUnit.DAYS.between(dueAt, returnedAt);
        // A partial day overdue still counts as a full day late.
        daysLate = Math.max(daysLate, 1);

        double fee = daysLate * LATE_FEE_PER_DAY;
        return Math.min(fee, MAX_LATE_FEE);
    }
}
