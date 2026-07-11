from pathlib import Path

from langchain_core.documents import Document
from langchain_community.document_loaders import TextLoader


class RepositoryLoader:
    SUPPORTED_EXTENSIONS = {
        ".py",
        ".md",
        ".txt",
        ".json",
        ".yaml",
        ".yml",
        ".toml",
        ".ini",
        ".html",
        ".css",
        ".js",
        ".ts",
        ".tsx",
        ".jsx",
        ".java",
        ".cpp",
        ".c",
        ".h",
        ".go",
        ".rs",
        ".sql",
        ".sh",
    }

    def load(self, repository_path: Path, files: list[Path]) -> list[Document]:

        documents: list[Document] = []

        for relative_path in files:
            absolute_path = repository_path / relative_path

            if absolute_path.suffix.lower() not in self.SUPPORTED_EXTENSIONS:
                continue

            loader = TextLoader(
                str(absolute_path),
                encoding="utf-8",
            )

            document = loader.load()[0]

            document.metadata.update(
                {
                    "file_path": str(relative_path),
                    "extension": absolute_path.suffix.lower(),
                }
            )

            documents.append(document)

        return documents