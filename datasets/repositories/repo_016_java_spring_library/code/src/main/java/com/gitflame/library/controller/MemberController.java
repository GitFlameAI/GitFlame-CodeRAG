package com.gitflame.library.controller;

import com.gitflame.library.model.Member;
import com.gitflame.library.repository.MemberRepository;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.time.LocalDateTime;
import java.util.NoSuchElementException;

@RestController
@RequestMapping("/members")
public class MemberController {

    private final MemberRepository memberRepository;

    public MemberController(MemberRepository memberRepository) {
        this.memberRepository = memberRepository;
    }

    @PostMapping
    public Member registerMember(@RequestBody Member member) {
        member.setId(null);
        member.setRegisteredAt(LocalDateTime.now());
        return memberRepository.save(member);
    }

    @GetMapping("/{id}")
    public Member getMember(@PathVariable Long id) {
        return memberRepository.findById(id)
                .orElseThrow(() -> new NoSuchElementException("Member not found: " + id));
    }
}
