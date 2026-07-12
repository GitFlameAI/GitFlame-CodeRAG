/// A small set of ignore patterns, matched with simple glob-free
/// suffix/prefix rules (no external glob crate available).
pub struct IgnoreList {
    patterns: Vec<String>,
}

impl IgnoreList {
    pub fn new(patterns: Vec<String>) -> Self {
        IgnoreList { patterns }
    }

    /// Returns true when `name` matches one of the configured patterns.
    /// Supports a leading `*` for suffix matches (e.g. `*.log`) and a
    /// trailing `*` for prefix matches (e.g. `target*`); anything else is
    /// compared exactly.
    pub fn is_ignored(&self, name: &str) -> bool {
        self.patterns.iter().any(|pattern| match pattern.as_bytes() {
            [b'*', rest @ ..] => name.ends_with(std::str::from_utf8(rest).unwrap_or("")),
            [rest @ .., b'*'] => name.starts_with(std::str::from_utf8(rest).unwrap_or("")),
            _ => name == pattern,
        })
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn matches_suffix_pattern() {
        let list = IgnoreList::new(vec!["*.log".to_string()]);
        assert!(list.is_ignored("debug.log"));
        assert!(!list.is_ignored("debug.txt"));
    }

    #[test]
    fn matches_prefix_pattern() {
        let list = IgnoreList::new(vec!["target*".to_string()]);
        assert!(list.is_ignored("target-dir"));
    }
}
