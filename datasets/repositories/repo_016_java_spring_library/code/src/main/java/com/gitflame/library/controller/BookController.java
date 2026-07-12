package com.gitflame.library.controller;

import com.gitflame.library.model.Book;
import com.gitflame.library.service.CatalogService;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/books")
public class BookController {

    private final CatalogService catalogService;

    public BookController(CatalogService catalogService) {
        this.catalogService = catalogService;
    }

    @GetMapping
    public List<Book> listBooks() {
        return catalogService.listBooks();
    }

    @GetMapping("/{id}")
    public Book getBook(@PathVariable Long id) {
        return catalogService.getBook(id);
    }

    @GetMapping("/search")
    public List<Book> search(@RequestParam String query) {
        return catalogService.search(query);
    }
}
