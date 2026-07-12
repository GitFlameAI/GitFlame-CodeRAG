use crate::counter::Stats;

/// Alternative CSV output format, independent of `report::render`.
pub fn render_csv(stats: &Stats) -> String {
    format!(
        "files,lines,bytes\n{},{},{}",
        stats.files, stats.lines, stats.bytes
    )
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::counter::Stats;

    #[test]
    fn writes_header_and_values() {
        let stats = Stats {
            files: 2,
            lines: 10,
            bytes: 100,
        };
        assert_eq!(render_csv(&stats), "files,lines,bytes\n2,10,100");
    }
}
