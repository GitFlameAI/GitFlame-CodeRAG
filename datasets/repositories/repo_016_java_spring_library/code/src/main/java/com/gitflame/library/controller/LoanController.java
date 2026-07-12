package com.gitflame.library.controller;

import com.gitflame.library.dto.BorrowRequest;
import com.gitflame.library.dto.LoanResponse;
import com.gitflame.library.model.Loan;
import com.gitflame.library.service.LoanService;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/loans")
public class LoanController {

    private final LoanService loanService;

    public LoanController(LoanService loanService) {
        this.loanService = loanService;
    }

    @PostMapping("/borrow")
    public LoanResponse borrow(@RequestBody BorrowRequest request) {
        Loan loan = loanService.borrowBook(request.getBookId(), request.getMemberId());
        return LoanResponse.from(loan);
    }

    @PostMapping("/{id}/return")
    public LoanResponse returnLoan(@PathVariable Long id) {
        Loan loan = loanService.returnBook(id);
        return LoanResponse.from(loan);
    }
}
