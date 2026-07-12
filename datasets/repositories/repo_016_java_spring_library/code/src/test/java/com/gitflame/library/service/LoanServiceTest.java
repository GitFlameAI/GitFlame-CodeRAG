package com.gitflame.library.service;

import com.gitflame.library.model.Book;
import com.gitflame.library.model.Loan;
import com.gitflame.library.model.Member;
import com.gitflame.library.repository.BookRepository;
import com.gitflame.library.repository.LoanRepository;
import com.gitflame.library.repository.MemberRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.time.LocalDateTime;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;

class LoanServiceTest {

    private BookRepository bookRepository;
    private MemberRepository memberRepository;
    private LoanRepository loanRepository;
    private LoanService loanService;

    @BeforeEach
    void setUp() {
        bookRepository = new BookRepository();
        memberRepository = new MemberRepository();
        loanRepository = new LoanRepository();
        loanService = new LoanService(loanRepository, bookRepository, memberRepository);
    }

    @Test
    void borrowingAvailableBookCreatesLoan() {
        Book book = bookRepository.save(new Book(null, "978-0-13-468599-1", "Effective Java", "Joshua Bloch", 2));
        Member member = memberRepository.save(new Member(null, "Ada Lovelace", "ada@example.com", LocalDateTime.now()));

        Loan loan = loanService.borrowBook(book.getId(), member.getId());

        assertNotNull(loan.getId());
        assertEquals(book.getId(), loan.getBookId());
        assertEquals(member.getId(), loan.getMemberId());
        assertEquals(false, loan.isReturned());
    }

    @Test
    void borrowingBookDecrementsAvailableCopiesByOne() {
        Book book = bookRepository.save(new Book(null, "978-0-596-00712-6", "Head First Design Patterns", "Freeman & Robson", 3));
        Member member = memberRepository.save(new Member(null, "Grace Hopper", "grace@example.com", LocalDateTime.now()));

        loanService.borrowBook(book.getId(), member.getId());

        Book updated = bookRepository.findById(book.getId()).orElseThrow();
        assertEquals(2, updated.getAvailableCopies());
    }
}
