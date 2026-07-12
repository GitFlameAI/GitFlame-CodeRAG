use std::time::Duration;

/// Configuration for a future `--watch` mode that would re-run the counter
/// on an interval; not wired into `main` yet.
pub struct WatchConfig {
    pub interval: Duration,
    pub max_iterations: Option<u32>,
}

impl WatchConfig {
    pub fn new(interval_secs: u64) -> Self {
        WatchConfig {
            interval: Duration::from_secs(interval_secs),
            max_iterations: None,
        }
    }

    pub fn limited(interval_secs: u64, max_iterations: u32) -> Self {
        WatchConfig {
            interval: Duration::from_secs(interval_secs),
            max_iterations: Some(max_iterations),
        }
    }

    /// Whether another poll should run given how many have already happened.
    pub fn should_continue(&self, iterations_done: u32) -> bool {
        match self.max_iterations {
            Some(max) => iterations_done < max,
            None => true,
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn stops_after_max_iterations() {
        let cfg = WatchConfig::limited(1, 3);
        assert!(cfg.should_continue(2));
        assert!(!cfg.should_continue(3));
    }

    #[test]
    fn runs_forever_without_a_limit() {
        let cfg = WatchConfig::new(5);
        assert!(cfg.should_continue(1000));
    }
}
