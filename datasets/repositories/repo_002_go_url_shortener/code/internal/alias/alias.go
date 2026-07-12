package alias

import (
	"errors"
	"sync"
)

// ErrTaken is returned when a caller tries to reserve an alias that is
// already in use.
var ErrTaken = errors.New("alias already taken")

// Registry tracks custom short-link aliases that have been reserved.
type Registry struct {
	mu    sync.Mutex
	taken map[string]bool
}

// NewRegistry creates an empty alias registry.
func NewRegistry() *Registry {
	return &Registry{taken: make(map[string]bool)}
}

// Reserve claims alias for exclusive use, failing if it is already taken.
func (r *Registry) Reserve(alias string) error {
	r.mu.Lock()
	defer r.mu.Unlock()
	if r.taken[alias] {
		return ErrTaken
	}
	r.taken[alias] = true
	return nil
}

// Available reports whether alias has not yet been reserved.
func (r *Registry) Available(alias string) bool {
	r.mu.Lock()
	defer r.mu.Unlock()
	return !r.taken[alias]
}
