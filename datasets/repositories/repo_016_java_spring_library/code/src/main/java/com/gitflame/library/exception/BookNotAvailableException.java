package com.gitflame.library.exception;

/** Thrown when a member attempts to borrow a book with no copies currently available. */
public class BookNotAvailableException extends RuntimeException {

    public BookNotAvailableException(String message) {
        super(message);
    }
}
