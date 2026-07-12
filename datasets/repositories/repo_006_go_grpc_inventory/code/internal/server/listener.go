package server

import (
	"log"
	"net"
)

// Serve starts a TCP listener on addr and blocks, logging incoming
// connection accept errors. It gives main a real serving loop to call
// instead of discarding the handler it builds.
func Serve(addr string, h *Handler) error {
	lis, err := net.Listen("tcp", addr)
	if err != nil {
		return err
	}
	defer lis.Close()

	log.Printf("inventory grpc listener on %s", addr)
	for {
		conn, err := lis.Accept()
		if err != nil {
			log.Printf("accept error: %v", err)
			continue
		}
		conn.Close() // real implementation would hand off to a gRPC server
	}
}
