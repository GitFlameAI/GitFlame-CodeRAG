/// Usage text for `--help` / `-h`.
///
/// `cli::parse` does not currently recognise a help flag before rejecting
/// unknown ones; printing this from `main` on `-h`/`--help` is the fix for
/// the missing help output.
pub const USAGE: &str = "\
rust-cli-linecount [OPTIONS] [PATH]

OPTIONS:
    -r, --recursive   recurse into subdirectories
        --json        print stats as JSON
    -h, --help        print this help text

PATH defaults to the current directory.";

pub fn print_help() {
    println!("{USAGE}");
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn usage_mentions_all_flags() {
        assert!(USAGE.contains("--recursive"));
        assert!(USAGE.contains("--json"));
        assert!(USAGE.contains("--help"));
    }
}
