package category

// Category groups items under a named classification, e.g. "electronics".
type Category struct {
	Name string
	SKUs []string
}

// Index maps category names to the SKUs assigned to them.
type Index struct {
	byName map[string]*Category
}

// NewIndex creates an empty category index.
func NewIndex() *Index {
	return &Index{byName: make(map[string]*Category)}
}

// Add assigns sku to the named category, creating it if necessary.
func (i *Index) Add(name, sku string) {
	c, ok := i.byName[name]
	if !ok {
		c = &Category{Name: name}
		i.byName[name] = c
	}
	c.SKUs = append(c.SKUs, sku)
}

// SKUsIn returns the SKUs assigned to the named category.
func (i *Index) SKUsIn(name string) []string {
	c, ok := i.byName[name]
	if !ok {
		return nil
	}
	return c.SKUs
}
