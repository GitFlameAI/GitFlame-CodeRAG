package com.gitflame.library.service;

import com.gitflame.library.model.Book;
import com.gitflame.library.repository.BookRepository;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.NoSuchElementException;

@Service
public class CatalogService {

    private final BookRepository bookRepository;

    public CatalogService(BookRepository bookRepository) {
        this.bookRepository = bookRepository;
    }

    public List<Book> listBooks() {
        return bookRepository.findAll();
    }

    public Book getBook(Long id) {
        return bookRepository.findById(id)
                .orElseThrow(() -> new NoSuchElementException("Book not found: " + id));
    }

    /** Case-insensitive search across title and author. */
    public List<Book> search(String query) {
        String needle = query.toLowerCase();
        return bookRepository.findAll().stream()
                .filter(book -> book.getTitle().toLowerCase().contains(needle)
                        || book.getAuthor().toLowerCase().contains(needle))
                .toList();
    }
}
