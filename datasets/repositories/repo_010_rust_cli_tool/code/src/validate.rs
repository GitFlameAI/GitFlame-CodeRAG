use std::path::Path;

/// Confirms `path` exists before counting begins.
///
/// Returns an error message suitable for printing to stderr; callers should
/// exit with a non-zero status when this fails instead of letting
/// `count_path` silently return zeroed-out stats for a missing path.
pub fn path_exists(path: &str) -> Result<(), String> {
    if Path::new(path).exists() {
        Ok(())
    } else {
        Err(format!("path not found: {path}"))
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn missing_path_is_an_error() {
        assert!(path_exists("/definitely/does/not/exist").is_err());
    }

    #[test]
    fn existing_path_is_ok() {
        assert!(path_exists(".").is_ok());
    }
}
