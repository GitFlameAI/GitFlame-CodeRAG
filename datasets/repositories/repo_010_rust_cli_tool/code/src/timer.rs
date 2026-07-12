use std::time::Instant;

/// Measures how long a scan takes; a building block for a future `--timing`
/// flag that would print elapsed time alongside the stats.
pub struct ScanTimer {
    started: Instant,
}

impl ScanTimer {
    pub fn start() -> Self {
        ScanTimer {
            started: Instant::now(),
        }
    }

    pub fn elapsed_ms(&self) -> u128 {
        self.started.elapsed().as_millis()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn elapsed_ms_is_bounded_for_a_fresh_timer() {
        let timer = ScanTimer::start();
        assert!(timer.elapsed_ms() < 60_000);
    }
}
