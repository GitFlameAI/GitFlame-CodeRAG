package validate

import "strings"

// URL reports whether s looks like a usable absolute URL.
// It rejects empty strings and values missing a scheme, which is the
// root cause of dangling short codes created by handleShorten.
func URL(s string) bool {
	s = strings.TrimSpace(s)
	if s == "" {
		return false
	}
	return strings.HasPrefix(s, "http://") || strings.HasPrefix(s, "https://")
}
