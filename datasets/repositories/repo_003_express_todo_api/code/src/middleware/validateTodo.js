function validateTodo(req, res, next) {
  const { title } = req.body || {};
  if (typeof title !== "string" || title.trim().length === 0) {
    return res.status(400).json({ error: "title is required" });
  }
  next();
}

module.exports = { validateTodo };
