use std::fs;
use std::path::Path;

/// Returns true if `path` is a symlink, without following it.
///
/// `Path::is_dir` / `Path::is_file` follow symlinks, so callers that want to
/// avoid recursing into symlinked directories (and risking a cycle) should
/// check this before descending.
pub fn is_symlink(path: &Path) -> bool {
    fs::symlink_metadata(path)
        .map(|meta| meta.file_type().is_symlink())
        .unwrap_or(false)
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::path::Path;

    #[test]
    fn missing_path_is_not_reported_as_a_symlink() {
        assert!(!is_symlink(Path::new("/definitely/does/not/exist")));
    }
}
