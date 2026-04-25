import argparse
import logging
import sys
from pathlib import Path
from src.config import DEFAULT_TARGET
from src.organizer import FileOrganizer

def setup_logging(log_file: Path) -> None:
    """Setup logging to file and console."""
    import logging
    
    # Get root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    
    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    
    # Add file handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)
    
    # Add stream handler
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    root_logger.addHandler(stream_handler)

def main():
    parser = argparse.ArgumentParser(description="Organize files in a directory by categories.")
    parser.add_argument(
        "--target",
        type=Path,
        default=DEFAULT_TARGET,
        help=f"Target directory to organize (default: {DEFAULT_TARGET})"
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Apply the organization (default is dry-run mode)"
    )
    
    args = parser.parse_args()
    
    # Setup logging
    log_file = Path(__file__).parent.parent / "logs" / "organizer.log"
    setup_logging(log_file)
    
    logger = logging.getLogger(__name__)
    logger.info(f"Starting file organizer on {args.target}, apply={args.apply}")
    
    # Create organizer
    dry_run = not args.apply
    organizer = FileOrganizer(args.target, dry_run=dry_run)
    
    # Scan and plan
    organizer.scan_and_plan()
    
    # Print summary
    print(organizer.get_summary())
    
    # Execute
    organizer.execute()
    
    logger.info("File organization completed.")

if __name__ == "__main__":
    main()