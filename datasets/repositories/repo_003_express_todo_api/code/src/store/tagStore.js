const tagsByTodoId = new Map();

function addTag(todoId, tag) {
  const tags = tagsByTodoId.get(todoId) || new Set();
  tags.add(tag);
  tagsByTodoId.set(todoId, tags);
  return Array.from(tags);
}

function listTags(todoId) {
  return Array.from(tagsByTodoId.get(todoId) || []);
}

function removeTag(todoId, tag) {
  const tags = tagsByTodoId.get(todoId);
  if (!tags) return false;
  return tags.delete(tag);
}

module.exports = { addTag, listTags, removeTag };
