package com.gitflame.library.repository;

import com.gitflame.library.model.Loan;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicLong;
import java.util.stream.Collectors;

@Repository
public class LoanRepository {

    private final Map<Long, Loan> loans = new ConcurrentHashMap<>();
    private final AtomicLong idSequence = new AtomicLong(1);

    public Loan save(Loan loan) {
        if (loan.getId() == null) {
            loan.setId(idSequence.getAndIncrement());
        }
        loans.put(loan.getId(), loan);
        return loan;
    }

    public Optional<Loan> findById(Long id) {
        return Optional.ofNullable(loans.get(id));
    }

    public List<Loan> findAll() {
        return List.copyOf(loans.values());
    }

    public List<Loan> findByMemberId(Long memberId) {
        return loans.values().stream()
                .filter(loan -> loan.getMemberId().equals(memberId))
                .collect(Collectors.toList());
    }

    /** Loans whose due date has passed. Used to drive overdue reminder emails. */
    public List<Loan> findOverdueLoans() {
        LocalDateTime now = LocalDateTime.now();
        return loans.values().stream()
                .filter(loan -> loan.getDueAt().isBefore(now))
                .collect(Collectors.toList());
    }
}
