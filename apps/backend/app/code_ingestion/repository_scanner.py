from pathlib import Path


SUPPORTED_EXTENSIONS = {
    ".py",
    ".ts",
    ".tsx",
    ".js",
    ".jsx",
    ".java",
    ".go",
    ".rs",
    ".cpp",
    ".c",
}


IGNORED_DIRECTORIES = {
    ".git",
    ".venv",
    "venv",
    "node_modules",
    "__pycache__",
    ".next",
    ".turbo",
    ".vercel",
    ".cache",
    "coverage",
    "dist",
    "build",
    "out",
    ".idea",
    ".vscode",
    ".pytest_cache",
    ".mypy_cache",
}


class RepositoryScanner:
    def scan(
        self,
        repository_root: Path,
    ) -> list[Path]:

        files: list[Path] = []

        for path in repository_root.rglob("*"):

            if any(
                ignored in path.parts
                for ignored in IGNORED_DIRECTORIES
            ):
                continue

            if (
                path.is_file()
                and path.suffix in SUPPORTED_EXTENSIONS
            ):
                files.append(path)

        return files