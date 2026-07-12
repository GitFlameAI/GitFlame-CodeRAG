package app

import "net/http"

// requireMethod wraps a handler so it only runs for the given HTTP
// method, responding 405 for anything else.
func requireMethod(method string, next http.HandlerFunc) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		if r.Method != method {
			http.Error(w, "method not allowed", http.StatusMethodNotAllowed)
			return
		}
		next(w, r)
	}
}
