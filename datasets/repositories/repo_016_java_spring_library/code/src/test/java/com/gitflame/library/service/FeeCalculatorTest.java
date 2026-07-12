package com.gitflame.library.service;

import org.junit.jupiter.api.Test;

import java.time.LocalDateTime;

import static org.junit.jupiter.api.Assertions.assertEquals;

class FeeCalculatorTest {

    private final FeeCalculator feeCalculator = new FeeCalculator();

    @Test
    void chargesExpectedFeeForGenuinelyLateReturn() {
        LocalDateTime dueAt = LocalDateTime.of(2026, 3, 1, 17, 0);
        LocalDateTime returnedAt = dueAt.plusDays(3);

        double fee = feeCalculator.calculateLateFee(dueAt, returnedAt);

        assertEquals(0.75, fee, 0.001);
    }

    @Test
    void earlyReturnIncursNoFee() {
        LocalDateTime dueAt = LocalDateTime.of(2026, 3, 1, 17, 0);
        LocalDateTime returnedAt = dueAt.minusDays(2);

        double fee = feeCalculator.calculateLateFee(dueAt, returnedAt);

        assertEquals(0.0, fee, 0.001);
    }
}
