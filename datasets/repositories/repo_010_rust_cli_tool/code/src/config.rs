use std::collections::HashMap;

/// Parses a very small `key=value` config file format, one pair per line,
/// with `#` starting a comment. Intended for a future `.linecountrc`.
pub fn parse_config(contents: &str) -> HashMap<String, String> {
    let mut values = HashMap::new();
    for line in contents.lines() {
        let line = line.trim();
        if line.is_empty() || line.starts_with('#') {
            continue;
        }
        if let Some((key, value)) = line.split_once('=') {
            values.insert(key.trim().to_string(), value.trim().to_string());
        }
    }
    values
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn parses_pairs_and_skips_comments() {
        let cfg = parse_config("# comment\nrecursive=true\njson = false\n");
        assert_eq!(cfg.get("recursive").map(String::as_str), Some("true"));
        assert_eq!(cfg.get("json").map(String::as_str), Some("false"));
    }

    #[test]
    fn ignores_blank_lines() {
        let cfg = parse_config("\n\nrecursive=true\n\n");
        assert_eq!(cfg.len(), 1);
    }
}
