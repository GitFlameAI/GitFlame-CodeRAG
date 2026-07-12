export function sortByPinned(notes) {
  return [...notes].sort((a, b) => Number(b.pinned) - Number(a.pinned));
}
