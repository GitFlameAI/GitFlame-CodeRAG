package repo

import "errors"

// ErrItemNotFound is returned by operations that mutate an existing
// item, such as Delete, when the SKU is not present.
var ErrItemNotFound = errors.New("item not found")
