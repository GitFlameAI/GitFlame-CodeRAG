package reservation

import (
	"errors"
	"sync"
)

// ErrOverReserved is returned when a reservation would exceed the
// available quantity passed to Reserve.
var ErrOverReserved = errors.New("reservation exceeds available quantity")

// Book tracks quantities reserved per SKU ahead of fulfillment.
type Book struct {
	mu       sync.Mutex
	reserved map[string]int
}

// NewBook creates an empty reservation book.
func NewBook() *Book {
	return &Book{reserved: make(map[string]int)}
}

// Reserve holds qty units of sku against available, failing if doing so
// would reserve more than is available.
func (b *Book) Reserve(sku string, qty, available int) error {
	b.mu.Lock()
	defer b.mu.Unlock()
	if b.reserved[sku]+qty > available {
		return ErrOverReserved
	}
	b.reserved[sku] += qty
	return nil
}

// Release frees qty previously reserved units of sku.
func (b *Book) Release(sku string, qty int) {
	b.mu.Lock()
	defer b.mu.Unlock()
	if b.reserved[sku] < qty {
		b.reserved[sku] = 0
		return
	}
	b.reserved[sku] -= qty
}
