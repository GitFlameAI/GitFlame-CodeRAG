import { Book } from "./repo/bookRepo";

export function searchBooksByTitle(books: Book[], query: string): Book[] {
  const needle = query.trim().toLowerCase();
  if (!needle) {
    return books;
  }
  return books.filter((b) => b.title.toLowerCase().includes(needle));
}
