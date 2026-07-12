package warehouse

import "sync"

// Location represents a physical storage location a SKU can be
// assigned to, e.g. "A1-03".
type Location struct {
	Code string
	Zone string
}

// LocationRepo tracks which location each SKU is stored in.
type LocationRepo struct {
	mu        sync.RWMutex
	locations map[string]Location
}

// NewLocationRepo creates an empty location repo.
func NewLocationRepo() *LocationRepo {
	return &LocationRepo{locations: make(map[string]Location)}
}

// Assign records that sku is stored at loc.
func (r *LocationRepo) Assign(sku string, loc Location) {
	r.mu.Lock()
	defer r.mu.Unlock()
	r.locations[sku] = loc
}

// LocationOf returns the location assigned to sku, if any.
func (r *LocationRepo) LocationOf(sku string) (Location, bool) {
	r.mu.RLock()
	defer r.mu.RUnlock()
	loc, ok := r.locations[sku]
	return loc, ok
}
