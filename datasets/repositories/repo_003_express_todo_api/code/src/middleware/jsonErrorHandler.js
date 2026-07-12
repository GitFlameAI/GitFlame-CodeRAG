function jsonErrorHandler(err, req, res, next) {
  if (err.type === "entity.parse.failed" || err instanceof SyntaxError) {
    err.status = 400;
    err.message = "invalid JSON body";
  }
  next(err);
}

module.exports = { jsonErrorHandler };
