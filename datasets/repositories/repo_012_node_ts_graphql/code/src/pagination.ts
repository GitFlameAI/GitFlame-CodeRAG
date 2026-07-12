export interface Page<T> {
  items: T[];
  endCursor: string | null;
  hasNextPage: boolean;
}

export function paginate<T extends { id: string }>(
  items: T[],
  first: number,
  after?: string,
): Page<T> {
  const startIndex = after ? items.findIndex((i) => i.id === after) + 1 : 0;
  const slice = items.slice(startIndex, startIndex + first);
  const endIndex = startIndex + slice.length;
  return {
    items: slice,
    endCursor: slice.length ? slice[slice.length - 1].id : null,
    hasNextPage: endIndex < items.length,
  };
}
