package service

import "errors"

// ErrInsufficientStock is returned when an adjustment would drive
// quantity below zero.
var ErrInsufficientStock = errors.New("insufficient stock")

// ApplyDelta computes qty+delta, rejecting any result below zero so
// callers can enforce a stock floor before persisting the change.
func ApplyDelta(qty, delta int) (int, error) {
	next := qty + delta
	if next < 0 {
		return 0, ErrInsufficientStock
	}
	return next, nil
}
