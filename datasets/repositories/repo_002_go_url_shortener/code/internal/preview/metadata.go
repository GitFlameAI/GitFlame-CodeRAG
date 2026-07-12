package preview

import "strings"

// Metadata holds link preview information extracted from an HTML page.
type Metadata struct {
	Title string
}

// ExtractTitle pulls the contents of the first <title> tag out of raw
// HTML, returning an empty string if none is present.
func ExtractTitle(html string) string {
	start := strings.Index(html, "<title>")
	if start == -1 {
		return ""
	}
	start += len("<title>")
	end := strings.Index(html[start:], "</title>")
	if end == -1 {
		return ""
	}
	return strings.TrimSpace(html[start : start+end])
}
