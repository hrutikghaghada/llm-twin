import os
import shutil
import subprocess
import tempfile
from pathlib import Path

from loguru import logger

from llm_twin.domain.documents import RepositoryDocument

from .base import BaseCrawler


class GithubCrawler(BaseCrawler):
    model = RepositoryDocument

    def __init__(self, ignore=(".git", ".toml", ".lock", ".png")) -> None:
        super().__init__()
        self._ignore = ignore

    def extract(self, link: str, **kwargs) -> None:
        old_model = self.model.find(link=link)
        if old_model is not None:
            logger.info(f"Repository already exists in the database: {link}")

            return

        logger.info(f"Starting scrapping GitHub repository: {link}")

        repo_name = link.rstrip("/").split("/")[-1]

        local_temp = Path(tempfile.mkdtemp())

        try:
            os.chdir(local_temp)
            subprocess.run(["git", "clone", link])

            repo_path = next(local_temp.iterdir())

            tree = {}
            for root, _, files in os.walk(repo_path):
                dir = Path(root).relative_to(repo_path)
                if str(dir).startswith(self._ignore):
                    continue

                for file in files:
                    if file.endswith(self._ignore):
                        continue

                    file_path = dir / file
                    file_absolute_path = repo_path / file_path
                    with file_absolute_path.open("r", errors="ignore") as f:
                        tree[str(file_path)] = f.read().replace(" ", "")

            user = kwargs["user"]
            instance = self.model(
                content=tree,
                name=repo_name,
                link=link,
                platform="github",
                author_id=user.id,
                author_full_name=user.full_name,
            )
            instance.save()

        except Exception:
            raise
        finally:
            shutil.rmtree(local_temp)

        logger.info(f"Finished scrapping GitHub repository: {link}")
