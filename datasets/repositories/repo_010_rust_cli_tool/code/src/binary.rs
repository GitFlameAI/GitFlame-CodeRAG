/// Heuristic binary-content sniff: treats a file as binary if it contains a
/// NUL byte within the first few KB, mirroring what `file`/git use. Callers
/// can use this to warn about (or explicitly opt into) skipped files
/// instead of letting `read_to_string` fail silently.
const SNIFF_LEN: usize = 8192;

pub fn is_binary(bytes: &[u8]) -> bool {
    let end = bytes.len().min(SNIFF_LEN);
    bytes[..end].contains(&0)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn text_is_not_binary() {
        assert!(!is_binary(b"hello world\n"));
    }

    #[test]
    fn nul_byte_marks_binary() {
        assert!(is_binary(b"hello\0world"));
    }

    #[test]
    fn empty_content_is_not_binary() {
        assert!(!is_binary(b""));
    }
}
