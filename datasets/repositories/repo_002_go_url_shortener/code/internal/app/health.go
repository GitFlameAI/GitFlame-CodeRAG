package app

import "net/http"

// handleHealthz reports basic liveness for load balancer probes.
func (s *Server) handleHealthz(w http.ResponseWriter, r *http.Request) {
	w.WriteHeader(http.StatusOK)
	w.Write([]byte("ok"))
}
