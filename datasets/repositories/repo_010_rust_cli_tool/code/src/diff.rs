use crate::counter::Stats;

/// Difference between two `Stats` snapshots, useful for comparing runs
/// across commits or before/after a refactor.
pub struct StatsDiff {
    pub files: i64,
    pub lines: i64,
    pub bytes: i64,
}

pub fn diff(before: &Stats, after: &Stats) -> StatsDiff {
    StatsDiff {
        files: after.files as i64 - before.files as i64,
        lines: after.lines as i64 - before.lines as i64,
        bytes: after.bytes as i64 - before.bytes as i64,
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::counter::Stats;

    #[test]
    fn reports_positive_and_negative_deltas() {
        let before = Stats {
            files: 5,
            lines: 100,
            bytes: 1000,
        };
        let after = Stats {
            files: 4,
            lines: 120,
            bytes: 900,
        };
        let d = diff(&before, &after);
        assert_eq!(d.files, -1);
        assert_eq!(d.lines, 20);
        assert_eq!(d.bytes, -100);
    }
}
