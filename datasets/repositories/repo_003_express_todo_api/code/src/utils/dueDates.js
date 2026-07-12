function isOverdue(dueDate, now = new Date()) {
  if (!dueDate) return false;
  return new Date(dueDate).getTime() < now.getTime();
}

function daysUntilDue(dueDate, now = new Date()) {
  if (!dueDate) return null;
  const ms = new Date(dueDate).getTime() - now.getTime();
  return Math.ceil(ms / (1000 * 60 * 60 * 24));
}

module.exports = { isOverdue, daysUntilDue };
