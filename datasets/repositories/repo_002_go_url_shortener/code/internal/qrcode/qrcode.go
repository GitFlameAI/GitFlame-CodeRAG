package qrcode

import "fmt"

// Placeholder renders a text stand-in for a QR code image until a real
// encoder is wired in. It keeps the API stable for callers.
func Placeholder(data string) string {
	return fmt.Sprintf("[qrcode:%s]", data)
}
