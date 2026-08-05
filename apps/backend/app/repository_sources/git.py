from pathlib import Path
import subprocess


class GitClient:
    def _run(
        self,
        command: list[str],
    ) -> subprocess.CompletedProcess[str]:
        try:
            return subprocess.run(
                command,
                check=True,
                capture_output=True,
                text=True,
                timeout=300,
            )

        except subprocess.CalledProcessError as exc:
            stderr = exc.stderr.strip() if exc.stderr else "Unknown git error"

            raise RuntimeError(
                f"Git command failed:\n{stderr}"
            ) from exc

        except FileNotFoundError as exc:
            raise RuntimeError(
                "Git is not installed or is not available on PATH."
            ) from exc

    def clone(
        self,
        repository_url: str,
        destination: Path,
    ) -> None:

        self._run(
            [
                "git",
                "clone",
                "--depth",
                "1",
                "--single-branch",
                repository_url,
                str(destination),
            ]
        )

    def pull(
        self,
        repository_root: Path,
    ) -> None:

        self._run(
            [
                "git",
                "-C",
                str(repository_root),
                "pull",
            ]
        )

    def checkout(
        self,
        repository_root: Path,
        branch: str,
    ) -> None:

        self._run(
            [
                "git",
                "-C",
                str(repository_root),
                "checkout",
                branch,
            ]
        )

    def current_branch(
        self,
        repository_root: Path,
    ) -> str:

        result = self._run(
            [
                "git",
                "-C",
                str(repository_root),
                "rev-parse",
                "--abbrev-ref",
                "HEAD",
            ]
        )

        return result.stdout.strip()

    def current_commit(
        self,
        repository_root: Path,
    ) -> str:

        result = self._run(
            [
                "git",
                "-C",
                str(repository_root),
                "rev-parse",
                "HEAD",
            ]
        )

        return result.stdout.strip()

    def version(
        self,
    ) -> str:

        result = self._run(
            [
                "git",
                "--version",
            ]
        )

        return result.stdout.strip()