from pathlib import Path

from app.ingestion.extractor import RepositoryExtractor
from app.ingestion.loader import RepositoryLoader
from app.ingestion.scanner import RepositoryScanner
from app.ingestion.splitter import RepositorySplitter
from app.vectorstore.indexer import RepositoryIndexer


class RepositoryIngestionPipeline:
    def __init__(self) -> None:
        self.extractor = RepositoryExtractor()
        self.scanner = RepositoryScanner()
        self.loader = RepositoryLoader()
        self.splitter = RepositorySplitter()
        self.indexer = RepositoryIndexer()

    def ingest(self, zip_path: Path) -> None:
        repository_path = self.extractor.extract(zip_path)

        print(f"Extracted repository: {repository_path}")

        files = self.scanner.scan(repository_path)

        print(f"Files scanned: {len(files)}")

        documents = self.loader.load(
            repository_path=repository_path,
            files=files,
        )

        print(f"Documents loaded: {len(documents)}")

        chunks = self.splitter.split(documents)

        print(f"Chunks created: {len(chunks)}")

        self.indexer.index(chunks)