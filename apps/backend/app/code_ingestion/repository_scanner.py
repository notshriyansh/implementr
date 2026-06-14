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
    "dist",
    "build",
    ".idea",
    ".vscode",
    ".mypy_cache",
    ".pytest_cache",
    "coverage",
}


class RepositoryScanner:
    def scan(
        self,
        repo_path: str,
    ) -> list[Path]:
        root = Path(repo_path)

        files = []

        for path in root.rglob("*"):
            if any(
                ignored in path.parts
                for ignored in (
                    IGNORED_DIRECTORIES
                )
            ):
                continue

            if (
                path.is_file()
                and path.suffix
                in SUPPORTED_EXTENSIONS
            ):
                files.append(path)

        return files