package server

import (
	"errors"

	"inventory/internal/service"
)

// notFoundError signals that a lookup should surface as gRPC NotFound
// rather than a generic failure.
type notFoundError struct{ err error }

func (e notFoundError) Error() string { return e.err.Error() }

// mapError translates known service errors into sentinel wrapper types
// the gRPC layer can turn into the right status code.
func mapError(err error) error {
	if errors.Is(err, service.ErrNotFound) {
		return notFoundError{err}
	}
	return err
}
