package service

import "sync"

// AuditStore keeps adjustment history in memory so AdjustStock has
// somewhere real to persist entries instead of dropping them.
type AuditStore struct {
	mu      sync.Mutex
	entries []AuditEntry
}

// NewAuditStore creates an empty audit store.
func NewAuditStore() *AuditStore {
	return &AuditStore{}
}

// Append records a new audit entry.
func (s *AuditStore) Append(entry AuditEntry) {
	s.mu.Lock()
	defer s.mu.Unlock()
	s.entries = append(s.entries, entry)
}

// ForSKU returns all recorded entries for the given SKU, in insertion order.
func (s *AuditStore) ForSKU(sku string) []AuditEntry {
	s.mu.Lock()
	defer s.mu.Unlock()
	var out []AuditEntry
	for _, e := range s.entries {
		if e.SKU == sku {
			out = append(out, e)
		}
	}
	return out
}
