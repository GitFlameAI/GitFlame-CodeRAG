package ratelimit

import (
	"sync"
	"time"
)

// Limiter is a simple fixed-window per-key request limiter, keyed by
// client IP.
type Limiter struct {
	mu       sync.Mutex
	max      int
	window   time.Duration
	counts   map[string]int
	windowAt map[string]time.Time
}

// New creates a Limiter allowing max requests per window for each key.
func New(max int, window time.Duration) *Limiter {
	return &Limiter{
		max:      max,
		window:   window,
		counts:   make(map[string]int),
		windowAt: make(map[string]time.Time),
	}
}

// Allow reports whether the request for key should proceed, resetting
// the window when it has elapsed.
func (l *Limiter) Allow(key string) bool {
	l.mu.Lock()
	defer l.mu.Unlock()

	now := time.Now()
	if start, ok := l.windowAt[key]; !ok || now.Sub(start) > l.window {
		l.windowAt[key] = now
		l.counts[key] = 0
	}
	l.counts[key]++
	return l.counts[key] <= l.max
}
