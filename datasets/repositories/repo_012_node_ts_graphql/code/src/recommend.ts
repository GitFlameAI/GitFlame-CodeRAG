import { Book } from "./repo/bookRepo";

export function recommendBooks(book: Book, allBooks: Book[], limit = 3): Book[] {
  return allBooks
    .filter((b) => b.authorId === book.authorId && b.id !== book.id)
    .slice(0, limit);
}
