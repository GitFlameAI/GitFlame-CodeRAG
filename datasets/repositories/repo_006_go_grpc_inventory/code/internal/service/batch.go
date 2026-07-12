package service

// Adjustment pairs a SKU with the delta to apply, used by batch
// operations that adjust several items in one call.
type Adjustment struct {
	SKU   string
	Delta int
}

// BatchResult captures the outcome of one adjustment within a batch.
type BatchResult struct {
	SKU string
	Err error
}

// ApplyBatch runs adjust for every item in adjustments and collects the
// per-item outcome instead of failing the whole batch on one error.
func ApplyBatch(adjustments []Adjustment, adjust func(sku string, delta int) error) []BatchResult {
	results := make([]BatchResult, 0, len(adjustments))
	for _, a := range adjustments {
		results = append(results, BatchResult{SKU: a.SKU, Err: adjust(a.SKU, a.Delta)})
	}
	return results
}
