package config

import "os"

const defaultPort = "8080"

// Port returns the PORT environment variable, falling back to the
// package default when it is unset or empty.
func Port() string {
	if p := os.Getenv("PORT"); p != "" {
		return p
	}
	return defaultPort
}
