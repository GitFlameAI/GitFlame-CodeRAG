package alert

import "inventory/internal/repo"

// Alert describes a SKU that has fallen at or below its reorder threshold.
type Alert struct {
	SKU      string
	Quantity int
}

// LowStock scans items and returns an Alert for every one at or below
// threshold.
func LowStock(items []*repo.Item, threshold int) []Alert {
	var alerts []Alert
	for _, it := range items {
		if it.Quantity <= threshold {
			alerts = append(alerts, Alert{SKU: it.SKU, Quantity: it.Quantity})
		}
	}
	return alerts
}
