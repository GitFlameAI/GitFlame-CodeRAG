export interface RequestContext {
  userId: string | null;
}

export function buildContext(headers: Record<string, string | undefined>): RequestContext {
  const token = headers["authorization"];
  if (!token) {
    return { userId: null };
  }
  return { userId: token.replace(/^Bearer\s+/i, "") };
}
