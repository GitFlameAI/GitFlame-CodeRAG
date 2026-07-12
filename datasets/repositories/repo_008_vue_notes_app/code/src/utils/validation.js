export function isBlankTitle(title) {
  return title.trim().length === 0;
}

export function assertValidTitle(title) {
  if (isBlankTitle(title)) {
    throw new Error("Title must not be empty");
  }
}
