"""Application level constants."""

from pathlib import Path

APP_NAME = "PDF Merger Pro"
DEFAULT_ENCODING = "utf-8"
PDF_EXTENSION = ".pdf"
SUPPORTED_EXTENSIONS = (PDF_EXTENSION,)
TIMESTAMP_PATTERN = "%Y%m%d_%H%M%S"
MAX_PREVIEW_FILES = 10
DEFAULT_DESTINATION = Path(".")
