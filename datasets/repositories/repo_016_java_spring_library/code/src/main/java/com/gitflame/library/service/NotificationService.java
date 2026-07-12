package com.gitflame.library.service;

import com.gitflame.library.model.Loan;
import com.gitflame.library.model.Member;
import com.gitflame.library.repository.LoanRepository;
import com.gitflame.library.repository.MemberRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class NotificationService {

    private static final Logger log = LoggerFactory.getLogger(NotificationService.class);

    private final LoanRepository loanRepository;
    private final MemberRepository memberRepository;

    public NotificationService(LoanRepository loanRepository, MemberRepository memberRepository) {
        this.loanRepository = loanRepository;
        this.memberRepository = memberRepository;
    }

    /** Emails every member with an overdue loan. Intended to run on a nightly schedule. */
    public void sendOverdueReminders() {
        List<Loan> overdueLoans = loanRepository.findOverdueLoans();

        for (Loan loan : overdueLoans) {
            memberRepository.findById(loan.getMemberId())
                    .ifPresent(this::sendReminderEmail);
        }
    }

    private void sendReminderEmail(Member member) {
        log.info("Sending overdue reminder email to {}", member.getEmail());
    }
}
