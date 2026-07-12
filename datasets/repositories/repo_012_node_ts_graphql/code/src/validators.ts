export function validateAuthorName(name: string): void {
  if (!name || !name.trim()) {
    throw new Error("author name must not be empty");
  }
}

export function validateBookTitle(title: string): void {
  if (!title || !title.trim()) {
    throw new Error("book title must not be empty");
  }
}
