from pathlib import Path
import subprocess


def clone_repository(
    repository_url: str,
    destination: Path,
    branch: str | None = None,
) -> None:
    command = [
        "git",
        "clone",
    ]

    if branch:
        command.extend(
            [
                "--branch",
                branch,
                "--single-branch",
            ]
        )

    command.extend(
        [
            repository_url,
            str(destination),
        ]
    )

    subprocess.run(
        command,
        check=True,
    )