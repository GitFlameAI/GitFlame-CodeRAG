import { Author, AuthorRepo } from "./authorRepo";

export class AuthorLoader {
  private cache = new Map<string, Author | undefined>();

  constructor(private readonly authors: AuthorRepo) {}

  load(id: string): Author | undefined {
    if (!this.cache.has(id)) {
      this.cache.set(id, this.authors.byId(id));
    }
    return this.cache.get(id);
  }

  loadMany(ids: string[]): (Author | undefined)[] {
    return ids.map((id) => this.load(id));
  }

  clear(): void {
    this.cache.clear();
  }
}
