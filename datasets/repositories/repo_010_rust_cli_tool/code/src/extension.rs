use std::path::Path;

/// Returns the lowercase extension of `path`, or "noext" when there isn't
/// one, so it can be used directly as a per-extension breakdown key.
pub fn extension_of(path: &Path) -> String {
    path.extension()
        .and_then(|ext| ext.to_str())
        .map(|ext| ext.to_lowercase())
        .unwrap_or_else(|| "noext".to_string())
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::path::Path;

    #[test]
    fn extracts_extension() {
        assert_eq!(extension_of(Path::new("src/main.rs")), "rs");
    }

    #[test]
    fn falls_back_when_missing() {
        assert_eq!(extension_of(Path::new("Makefile")), "noext");
    }

    #[test]
    fn lowercases_mixed_case_extensions() {
        assert_eq!(extension_of(Path::new("README.MD")), "md");
    }
}
