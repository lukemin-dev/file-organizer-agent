import logging
import shutil
from pathlib import Path
from typing import List, Tuple
from src.config import CATEGORIES
from src.utils import get_category, get_unique_name

logger = logging.getLogger(__name__)

class FileOrganizer:
    def __init__(self, target_dir: Path, dry_run: bool = True):
        self.target_dir = target_dir
        self.dry_run = dry_run
        self.actions: List[Tuple[Path, Path]] = []  # List of (source, destination)

    def scan_and_plan(self) -> None:
        """Scan the target directory and plan the organization."""
        if not self.target_dir.exists():
            logger.warning(f"Target directory {self.target_dir} does not exist.")
            return

        try:
            for file_path in self.target_dir.iterdir():
                if file_path.is_file() and not file_path.name.startswith('.'):
                    self._plan_file_move(file_path)
        except PermissionError:
            logger.error(f"Permission denied accessing directory {self.target_dir}")
            return

    def _plan_file_move(self, file_path: Path) -> None:
        """Plan the move for a single file."""
        extension = file_path.suffix
        category = get_category(extension)
        
        category_dir = self.target_dir / category
        unique_name = get_unique_name(category_dir, file_path.name)
        destination = category_dir / unique_name
        
        self.actions.append((file_path, destination))

    def execute(self) -> None:
        """Execute the planned actions."""
        for source, destination in self.actions:
            if self.dry_run:
                logger.info(f"DRY RUN: Would move {source} to {destination}")
                print(f"Would move {source.name} to {destination.parent.name}/{destination.name}")
            else:
                # Create category directory if it doesn't exist
                destination.parent.mkdir(exist_ok=True)
                shutil.move(str(source), str(destination))
                logger.info(f"Moved {source} to {destination}")
                print(f"Moved {source.name} to {destination.parent.name}/{destination.name}")

    def get_summary(self) -> str:
        """Get a summary of the actions."""
        if not self.actions:
            return "No files to organize."
        
        summary = f"Planned to organize {len(self.actions)} files:\n"
        category_counts = {}
        for _, dest in self.actions:
            category = dest.parent.name
            category_counts[category] = category_counts.get(category, 0) + 1
        
        for category, count in category_counts.items():
            summary += f"  {category}: {count} files\n"
        return summary