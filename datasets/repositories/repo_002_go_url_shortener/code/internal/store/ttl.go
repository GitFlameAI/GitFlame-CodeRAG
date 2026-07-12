package store

import "time"

// expiry tracks when a saved URL should be considered stale.
type expiry struct {
	at time.Time
}

// expired reports whether the given expiry has passed relative to now.
func (e expiry) expired(now time.Time) bool {
	return !e.at.IsZero() && now.After(e.at)
}

// newExpiry returns an expiry ttl duration from now, or a zero expiry
// (never expires) when ttl is zero or negative.
func newExpiry(ttl time.Duration) expiry {
	if ttl <= 0 {
		return expiry{}
	}
	return expiry{at: time.Now().Add(ttl)}
}
