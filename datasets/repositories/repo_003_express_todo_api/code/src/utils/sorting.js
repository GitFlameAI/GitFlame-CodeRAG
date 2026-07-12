function sortTodos(todos, field = "id", direction = "asc") {
  const sorted = [...todos].sort((a, b) => {
    if (a[field] < b[field]) return -1;
    if (a[field] > b[field]) return 1;
    return 0;
  });
  return direction === "desc" ? sorted.reverse() : sorted;
}

module.exports = { sortTodos };
