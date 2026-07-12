package repo

// UpdateQuantity atomically applies delta to the stored item's quantity
// under a single lock, avoiding the lost-update race that a separate
// Get followed by Put allows.
func (r *ItemRepo) UpdateQuantity(sku string, delta int) (int, error) {
	r.mu.Lock()
	defer r.mu.Unlock()

	item, ok := r.items[sku]
	if !ok {
		return 0, ErrItemNotFound
	}
	item.Quantity += delta
	return item.Quantity, nil
}
