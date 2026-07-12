const { sortTodos } = require("../src/utils/sorting");

test("sortTodos orders ascending by title", () => {
  const todos = [
    { id: 1, title: "b" },
    { id: 2, title: "a" },
  ];
  const sorted = sortTodos(todos, "title", "asc");
  expect(sorted.map((t) => t.title)).toEqual(["a", "b"]);
});

test("sortTodos orders descending by title", () => {
  const todos = [
    { id: 1, title: "b" },
    { id: 2, title: "a" },
  ];
  const sorted = sortTodos(todos, "title", "desc");
  expect(sorted.map((t) => t.title)).toEqual(["b", "a"]);
});
