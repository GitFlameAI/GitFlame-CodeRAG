/// Registry of flags recognised by the CLI parser.
pub const KNOWN_FLAGS: &[&str] = &["-r", "--recursive", "--json", "-h", "--help"];

/// Returns true if `flag` is a recognised CLI flag.
pub fn is_known(flag: &str) -> bool {
    KNOWN_FLAGS.contains(&flag)
}

/// Returns true if `arg` looks like a flag rather than a path (starts with
/// a dash). Useful for deciding whether an unrecognised argument should be
/// reported as a bad flag or treated as a path.
pub fn looks_like_flag(arg: &str) -> bool {
    arg.starts_with('-')
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn recognises_known_flags() {
        assert!(is_known("--json"));
        assert!(!is_known("--jsom"));
    }

    #[test]
    fn distinguishes_flags_from_paths() {
        assert!(looks_like_flag("--jsom"));
        assert!(!looks_like_flag("src"));
    }
}
