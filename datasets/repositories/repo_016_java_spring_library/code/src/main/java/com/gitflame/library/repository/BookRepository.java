package com.gitflame.library.repository;

import com.gitflame.library.model.Book;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicLong;

@Repository
public class BookRepository {

    private final Map<Long, Book> books = new ConcurrentHashMap<>();
    private final AtomicLong idSequence = new AtomicLong(1);

    public Book save(Book book) {
        if (book.getId() == null) {
            book.setId(idSequence.getAndIncrement());
        }
        books.put(book.getId(), book);
        return book;
    }

    public Optional<Book> findById(Long id) {
        return Optional.ofNullable(books.get(id));
    }

    public List<Book> findAll() {
        return List.copyOf(books.values());
    }

    public boolean existsByIsbn(String isbn) {
        return books.values().stream()
                .anyMatch(book -> book.getIsbn().equalsIgnoreCase(isbn));
    }
}
