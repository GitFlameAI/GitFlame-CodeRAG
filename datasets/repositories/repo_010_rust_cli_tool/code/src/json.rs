/// Minimal JSON string escaping helper, meant to replace the hand-rolled
/// formatting in `report::render` once it needs to emit string fields.
pub fn escape(value: &str) -> String {
    let mut out = String::with_capacity(value.len() + 2);
    for ch in value.chars() {
        match ch {
            '"' => out.push_str("\\\""),
            '\\' => out.push_str("\\\\"),
            '\n' => out.push_str("\\n"),
            '\t' => out.push_str("\\t"),
            c if (c as u32) < 0x20 => out.push_str(&format!("\\u{:04x}", c as u32)),
            c => out.push(c),
        }
    }
    out
}

/// Wraps a value in double quotes after escaping it.
pub fn quoted(value: &str) -> String {
    format!("\"{}\"", escape(value))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn escapes_quotes_and_backslashes() {
        assert_eq!(escape("a\"b\\c"), "a\\\"b\\\\c");
    }

    #[test]
    fn quoted_wraps_in_double_quotes() {
        assert_eq!(quoted("ok"), "\"ok\"");
    }
}
