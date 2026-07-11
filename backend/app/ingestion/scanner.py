from pathlib import Path


class RepositoryScanner:
    IGNORED_DIRECTORIES = {
        ".git",
        ".github",
        "node_modules",
        "venv",
        ".venv",
        "__pycache__",
        "dist",
        "build",
        ".idea",
        ".vscode",
    }

    def scan(self, repository_path: Path) -> list[Path]:
        """
        Recursively scan a repository and return all indexable files.
        """

        files: list[Path] = []

        for path in repository_path.rglob("*"):
            if not path.is_file():
                continue

            if any(part in self.IGNORED_DIRECTORIES for part in path.parts):
                continue

            files.append(path.relative_to(repository_path))

        return sorted(files)