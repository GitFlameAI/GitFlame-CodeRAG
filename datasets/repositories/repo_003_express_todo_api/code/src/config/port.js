function resolvePort(rawPort, fallback = 3000) {
  const port = Number.parseInt(rawPort, 10);
  if (!Number.isInteger(port) || port <= 0) {
    console.warn(`Invalid PORT "${rawPort}", falling back to ${fallback}`);
    return fallback;
  }
  return port;
}

module.exports = { resolvePort };
