import { AuthorRepo } from "./repo/authorRepo";
import { BookRepo } from "./repo/bookRepo";

export function seedSampleData(authors: AuthorRepo, books: BookRepo): void {
  authors.add({ id: "a1", name: "Ursula K. Le Guin" });
  authors.add({ id: "a2", name: "Isaac Asimov" });
  books.create("The Left Hand of Darkness", "a1");
  books.create("Foundation", "a2");
}
