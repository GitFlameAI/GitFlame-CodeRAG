package com.gitflame.library.dto;

import com.gitflame.library.model.Loan;

import java.time.LocalDateTime;

public class LoanResponse {

    private Long id;
    private Long bookId;
    private Long memberId;
    private LocalDateTime borrowedAt;
    private LocalDateTime dueAt;
    private LocalDateTime returnedAt;
    private boolean returned;

    public LoanResponse() {
    }

    public static LoanResponse from(Loan loan) {
        LoanResponse response = new LoanResponse();
        response.id = loan.getId();
        response.bookId = loan.getBookId();
        response.memberId = loan.getMemberId();
        response.borrowedAt = loan.getBorrowedAt();
        response.dueAt = loan.getDueAt();
        response.returnedAt = loan.getReturnedAt();
        response.returned = loan.isReturned();
        return response;
    }

    public Long getId() {
        return id;
    }

    public Long getBookId() {
        return bookId;
    }

    public Long getMemberId() {
        return memberId;
    }

    public LocalDateTime getBorrowedAt() {
        return borrowedAt;
    }

    public LocalDateTime getDueAt() {
        return dueAt;
    }

    public LocalDateTime getReturnedAt() {
        return returnedAt;
    }

    public boolean isReturned() {
        return returned;
    }
}
