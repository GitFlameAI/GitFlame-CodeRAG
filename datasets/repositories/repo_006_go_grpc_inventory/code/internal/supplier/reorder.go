package supplier

// Supplier is a source that can fulfill reorders for a SKU.
type Supplier struct {
	Name     string
	LeadDays int
}

// Suggestion recommends reordering qty units of a SKU from a supplier.
type Suggestion struct {
	SKU      string
	Supplier string
	Quantity int
}

// Suggest builds a reorder suggestion when quantity is below threshold,
// requesting enough stock to reach target.
func Suggest(sku string, quantity, threshold, target int, sup Supplier) *Suggestion {
	if quantity >= threshold {
		return nil
	}
	return &Suggestion{SKU: sku, Supplier: sup.Name, Quantity: target - quantity}
}
