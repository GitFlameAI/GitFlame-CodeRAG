function paginate(items, query = {}) {
  const limit = Number.parseInt(query.limit, 10);
  const offset = Number.parseInt(query.offset, 10);
  const safeLimit = Number.isFinite(limit) && limit > 0 ? limit : items.length;
  const safeOffset = Number.isFinite(offset) && offset > 0 ? offset : 0;
  return items.slice(safeOffset, safeOffset + safeLimit);
}

module.exports = { paginate };
