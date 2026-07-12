package store

import (
	"crypto/rand"
	"encoding/hex"
)

// Salt returns a short random hex string that can be mixed into a
// generated code so short codes stop being sequentially guessable.
func Salt(n int) string {
	buf := make([]byte, n)
	if _, err := rand.Read(buf); err != nil {
		// Fall back to a fixed, non-random salt rather than panicking;
		// callers should treat this as a degraded (not broken) path.
		for i := range buf {
			buf[i] = byte(i)
		}
	}
	return hex.EncodeToString(buf)
}
