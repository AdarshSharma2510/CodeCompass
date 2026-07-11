from pathlib import Path
import shutil
import zipfile


class RepositoryExtractor:
    def __init__(self, repository_dir: Path = Path("data/repository")) -> None:
        self.repository_dir = repository_dir

    def extract(self, zip_path: Path) -> Path:
        """ 
        Extract a repository ZIP into the repository directory.

        Returns:
            Path to the extracted repository.
        """

        if not zipfile.is_zipfile(zip_path):
            raise ValueError("Uploaded file is not a valid ZIP archive.")

        # Remove previously extracted repository
        if self.repository_dir.exists():
            shutil.rmtree(self.repository_dir)

        self.repository_dir.mkdir(parents=True, exist_ok=True)

        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(self.repository_dir)

        return self.repository_dir