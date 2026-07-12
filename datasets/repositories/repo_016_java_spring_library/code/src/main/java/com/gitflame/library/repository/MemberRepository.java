package com.gitflame.library.repository;

import com.gitflame.library.model.Member;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicLong;

@Repository
public class MemberRepository {

    private final Map<Long, Member> members = new ConcurrentHashMap<>();
    private final AtomicLong idSequence = new AtomicLong(1);

    public Member save(Member member) {
        if (member.getId() == null) {
            member.setId(idSequence.getAndIncrement());
        }
        members.put(member.getId(), member);
        return member;
    }

    public Optional<Member> findById(Long id) {
        return Optional.ofNullable(members.get(id));
    }

    public Optional<Member> findByEmail(String email) {
        return members.values().stream()
                .filter(member -> member.getEmail().equalsIgnoreCase(email))
                .findFirst();
    }

    public List<Member> findAll() {
        return List.copyOf(members.values());
    }
}
