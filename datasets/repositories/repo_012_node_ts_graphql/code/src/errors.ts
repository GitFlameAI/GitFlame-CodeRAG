export class NotFoundError extends Error {
  constructor(entity: string, id: string) {
    super(`${entity} not found: ${id}`);
    this.name = "NotFoundError";
  }
}

export class AuthorNotFoundError extends NotFoundError {
  constructor(id: string) {
    super("Author", id);
    this.name = "AuthorNotFoundError";
  }
}

export class BookNotFoundError extends NotFoundError {
  constructor(id: string) {
    super("Book", id);
    this.name = "BookNotFoundError";
  }
}
