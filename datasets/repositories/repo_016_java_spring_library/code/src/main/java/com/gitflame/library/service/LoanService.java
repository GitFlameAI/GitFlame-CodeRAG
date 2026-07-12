package com.gitflame.library.service;

import com.gitflame.library.exception.BookNotAvailableException;
import com.gitflame.library.model.Book;
import com.gitflame.library.model.Loan;
import com.gitflame.library.model.Member;
import com.gitflame.library.repository.BookRepository;
import com.gitflame.library.repository.LoanRepository;
import com.gitflame.library.repository.MemberRepository;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.NoSuchElementException;

import static com.gitflame.library.config.AppConfig.DEFAULT_LOAN_PERIOD_DAYS;

@Service
public class LoanService {

    private final LoanRepository loanRepository;
    private final BookRepository bookRepository;
    private final MemberRepository memberRepository;

    public LoanService(LoanRepository loanRepository, BookRepository bookRepository, MemberRepository memberRepository) {
        this.loanRepository = loanRepository;
        this.bookRepository = bookRepository;
        this.memberRepository = memberRepository;
    }

    public Loan borrowBook(Long bookId, Long memberId) {
        Book book = bookRepository.findById(bookId)
                .orElseThrow(() -> new NoSuchElementException("Book not found: " + bookId));
        Member member = memberRepository.findById(memberId)
                .orElseThrow(() -> new NoSuchElementException("Member not found: " + memberId));

        LocalDateTime now = LocalDateTime.now();
        Loan loan = new Loan(null, book.getId(), member.getId(), now, now.plusDays(DEFAULT_LOAN_PERIOD_DAYS));

        book.decrementAvailable();
        bookRepository.save(book);

        return loanRepository.save(loan);
    }

    public Loan returnBook(Long loanId) {
        Loan loan = loanRepository.findById(loanId)
                .orElseThrow(() -> new NoSuchElementException("Loan not found: " + loanId));

        loan.setReturned(true);
        loan.setReturnedAt(LocalDateTime.now());

        return loanRepository.save(loan);
    }

    private void assertAvailable(Book book) {
        if (book.getAvailableCopies() <= 0) {
            throw new BookNotAvailableException("No copies available for book: " + book.getId());
        }
    }
}
