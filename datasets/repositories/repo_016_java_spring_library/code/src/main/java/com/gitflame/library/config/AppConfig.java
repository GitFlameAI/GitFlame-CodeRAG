package com.gitflame.library.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.time.Clock;

@Configuration
public class AppConfig {

    /** Default number of days a member may keep a book before it is due. */
    public static final int DEFAULT_LOAN_PERIOD_DAYS = 14;

    /** Late fee charged per overdue day, in dollars. */
    public static final double LATE_FEE_PER_DAY = 0.25;

    /** Upper bound on the late fee a single loan can accrue. */
    public static final double MAX_LATE_FEE = 15.00;

    @Bean
    public Clock systemClock() {
        return Clock.systemDefaultZone();
    }
}
