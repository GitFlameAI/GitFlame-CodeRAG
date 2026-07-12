package importer

// Result captures the outcome of importing a single URL.
type Result struct {
	URL  string
	Code string
}

// saver is the minimal store capability bulk import needs.
type saver interface {
	Save(url string) string
}

// Bulk saves every url in urls using s, returning one Result per input
// in the same order.
func Bulk(s saver, urls []string) []Result {
	results := make([]Result, 0, len(urls))
	for _, u := range urls {
		code := s.Save(u)
		results = append(results, Result{URL: u, Code: code})
	}
	return results
}
