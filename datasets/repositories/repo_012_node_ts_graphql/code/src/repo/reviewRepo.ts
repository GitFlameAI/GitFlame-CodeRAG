export interface Review {
  id: string;
  bookId: string;
  rating: number;
  comment: string;
}

export class ReviewRepo {
  private reviews: Review[] = [];
  private seq = 1;

  add(bookId: string, rating: number, comment: string): Review {
    const review = { id: String(this.seq++), bookId, rating, comment };
    this.reviews.push(review);
    return review;
  }

  byBook(bookId: string): Review[] {
    return this.reviews.filter((r) => r.bookId === bookId);
  }

  averageRating(bookId: string): number | null {
    const ratings = this.byBook(bookId).map((r) => r.rating);
    if (ratings.length === 0) {
      return null;
    }
    return ratings.reduce((a, b) => a + b, 0) / ratings.length;
  }
}
