package app

import "strings"

// normalizeCode extracts the short code from a redirect path, trimming
// the "/r/" prefix as well as any trailing slash so "/r/abc" and
// "/r/abc/" resolve to the same stored code.
func normalizeCode(path string) string {
	code := strings.TrimPrefix(path, "/r/")
	return strings.TrimSuffix(code, "/")
}
