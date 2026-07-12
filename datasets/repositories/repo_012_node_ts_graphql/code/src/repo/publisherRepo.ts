export interface Publisher {
  id: string;
  name: string;
  country: string;
}

export class PublisherRepo {
  private publishers = new Map<string, Publisher>();

  add(publisher: Publisher): void {
    this.publishers.set(publisher.id, publisher);
  }

  byId(id: string): Publisher | undefined {
    return this.publishers.get(id);
  }

  all(): Publisher[] {
    return [...this.publishers.values()];
  }
}
