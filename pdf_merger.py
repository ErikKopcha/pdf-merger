#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 PDF Merger Pro - Advanced PDF Merging Tool
A powerful and beautiful command-line tool for merging PDF files from folders.

Features:
- Merge all PDFs from a specified folder
- Custom output naming or auto-naming based on folder
- Beautiful progress bars and colored output
- Recursive folder scanning
- Smart file sorting
- Error handling and validation

Usage:
    python3 pdf_merger_pro.py /path/to/folder
    python3 pdf_merger_pro.py /path/to/folder --output "Custom Name"
    python3 pdf_merger_pro.py /path/to/folder -o "Custom Name" --recursive
"""

import os
import sys
import argparse
from pathlib import Path
import re
from typing import List, Tuple, Optional
from datetime import datetime

# Color codes for beautiful terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Try to import PDF libraries
try:
    from pypdf import PdfWriter, PdfReader
    PDF_LIB = "pypdf"
except ImportError:
    try:
        from PyPDF2 import PdfWriter, PdfReader
        PDF_LIB = "PyPDF2"
    except ImportError:
        print(f"{Colors.FAIL}❌ Error: No PDF library found!{Colors.ENDC}")
        print(f"{Colors.WARNING}Please install one of the following:{Colors.ENDC}")
        print("  pip install pypdf")
        print("  pip install PyPDF2")
        sys.exit(1)

# Try to import progress bar library
try:
    from tqdm import tqdm
    HAS_TQDM = True
except ImportError:
    HAS_TQDM = False
    print(f"{Colors.WARNING}⚠️  Install 'tqdm' for beautiful progress bars: pip install tqdm{Colors.ENDC}")


def print_banner():
    """Print a beautiful banner"""
    banner = f"""
{Colors.HEADER}{Colors.BOLD}
╔══════════════════════════════════════════════════════════════╗
║                    🚀 PDF Merger Pro 🚀                     ║
║              Advanced PDF Merging Tool v2.0                 ║
║                                                              ║
║  Merge PDFs like a pro with style and efficiency!           ║
╚══════════════════════════════════════════════════════════════╝
{Colors.ENDC}"""
    print(banner)


def print_success(message: str):
    """Print success message with green color"""
    print(f"{Colors.OKGREEN}✅ {message}{Colors.ENDC}")


def print_error(message: str):
    """Print error message with red color"""
    print(f"{Colors.FAIL}❌ {message}{Colors.ENDC}")


def print_warning(message: str):
    """Print warning message with yellow color"""
    print(f"{Colors.WARNING}⚠️  {message}{Colors.ENDC}")


def print_info(message: str):
    """Print info message with blue color"""
    print(f"{Colors.OKBLUE}ℹ️  {message}{Colors.ENDC}")


def sanitize_filename(filename: str) -> str:
    """Sanitize filename by removing invalid characters"""
    # Remove invalid characters for filenames
    sanitized = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Remove multiple underscores
    sanitized = re.sub(r'_+', '_', sanitized)
    # Remove leading/trailing underscores and spaces
    sanitized = sanitized.strip('_ ')
    return sanitized


def get_pdf_files(folder_path: Path, recursive: bool = False) -> List[Path]:
    """
    Get all PDF files from the specified folder

    Args:
        folder_path: Path to the folder
        recursive: Whether to search recursively in subfolders

    Returns:
        List of PDF file paths sorted alphabetically
    """
    pdf_files = []

    if recursive:
        # Search recursively
        pdf_files = list(folder_path.rglob('*.pdf'))
    else:
        # Search only in the current folder
        pdf_files = list(folder_path.glob('*.pdf'))

    # Sort files alphabetically
    pdf_files.sort(key=lambda x: x.name.lower())

    return pdf_files


def merge_pdfs(pdf_files: List[Path], output_path: Path) -> bool:
    """
    Merge PDF files into a single PDF

    Args:
        pdf_files: List of PDF file paths to merge
        output_path: Path for the output PDF file

    Returns:
        True if successful, False otherwise
    """
    if not pdf_files:
        print_error("No PDF files found to merge!")
        return False

    print_info(f"Using {PDF_LIB} library for PDF processing")
    print_info(f"Merging {len(pdf_files)} PDF files...")

    # Create PDF writer
    pdf_writer = PdfWriter()
    total_pages = 0

    # Progress bar setup
    if HAS_TQDM:
        progress_bar = tqdm(pdf_files, desc="Processing PDFs", unit="file")
    else:
        progress_bar = pdf_files

    for i, pdf_path in enumerate(progress_bar):
        try:
            if not HAS_TQDM:
                print(f"  📄 Processing: {pdf_path.name} ({i+1}/{len(pdf_files)})")

            # Read PDF file
            with open(pdf_path, 'rb') as pdf_file:
                pdf_reader = PdfReader(pdf_file)
                pages_count = len(pdf_reader.pages)

                # Add all pages to the writer
                for page_num in range(pages_count):
                    page = pdf_reader.pages[page_num]
                    pdf_writer.add_page(page)

                total_pages += pages_count

                if HAS_TQDM:
                    progress_bar.set_postfix({
                        'Pages': total_pages,
                        'Current': f"{pages_count}p"
                    })
                else:
                    print(f"    ✓ Added {pages_count} pages")

        except Exception as e:
            print_error(f"Failed to process {pdf_path.name}: {str(e)}")
            continue

    # Write the merged PDF
    try:
        print_info(f"Saving merged PDF to: {output_path}")
        with open(output_path, 'wb') as output_file:
            pdf_writer.write(output_file)

        # Get file size
        file_size = output_path.stat().st_size
        file_size_mb = file_size / (1024 * 1024)

        print_success(f"Successfully created: {output_path.name}")
        print_info(f"Total pages: {total_pages}")
        print_info(f"File size: {file_size_mb:.2f} MB")

        return True

    except Exception as e:
        print_error(f"Failed to save merged PDF: {str(e)}")
        return False


def main():
    """Main function"""
    print_banner()

    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="🚀 PDF Merger Pro - Merge PDF files from a folder",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python pdf_merger_pro.py /path/to/folder
  python pdf_merger_pro.py /path/to/folder --output "My Merged Document"
  python pdf_merger_pro.py /path/to/folder -o "Custom Name" --recursive
  python pdf_merger_pro.py . --output "Current Folder PDFs"
        """
    )

    parser.add_argument(
        'folder_path',
        help='Path to the folder containing PDF files'
    )

    parser.add_argument(
        '-o', '--output',
        help='Custom name for the output PDF (without .pdf extension)',
        default=None
    )

    parser.add_argument(
        '-r', '--recursive',
        action='store_true',
        help='Search for PDFs recursively in subfolders'
    )

    parser.add_argument(
        '--destination',
        help='Destination folder for the output PDF (default: same as source)',
        default=None
    )

    # Parse arguments
    args = parser.parse_args()

    # Validate folder path
    folder_path = Path(args.folder_path).resolve()
    if not folder_path.exists():
        print_error(f"Folder does not exist: {folder_path}")
        sys.exit(1)

    if not folder_path.is_dir():
        print_error(f"Path is not a directory: {folder_path}")
        sys.exit(1)

    print_info(f"Source folder: {folder_path}")
    print_info(f"Recursive search: {'Yes' if args.recursive else 'No'}")

    # Get PDF files
    pdf_files = get_pdf_files(folder_path, args.recursive)

    if not pdf_files:
        print_warning("No PDF files found in the specified folder!")
        if not args.recursive:
            print_info("Try using --recursive flag to search in subfolders")
        sys.exit(0)

    print_success(f"Found {len(pdf_files)} PDF files")

    # Determine output filename
    if args.output:
        output_name = sanitize_filename(args.output)
    else:
        output_name = sanitize_filename(folder_path.name)

    # Ensure .pdf extension
    if not output_name.lower().endswith('.pdf'):
        output_name += '.pdf'

    # Determine output path
    if args.destination:
        destination_path = Path(args.destination).resolve()
        if not destination_path.exists():
            destination_path.mkdir(parents=True, exist_ok=True)
        output_path = destination_path / output_name
    else:
        output_path = folder_path / output_name

    # Check if output file already exists
    if output_path.exists():
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        name_without_ext = output_path.stem
        output_path = output_path.parent / f"{name_without_ext}_{timestamp}.pdf"
        print_warning(f"Output file exists, using: {output_path.name}")

    print_info(f"Output file: {output_path}")

    # Show file list
    print(f"\n{Colors.OKCYAN}📋 Files to merge:{Colors.ENDC}")
    for i, pdf_file in enumerate(pdf_files[:10], 1):  # Show first 10 files
        print(f"  {i:2d}. {pdf_file.name}")

    if len(pdf_files) > 10:
        print(f"  ... and {len(pdf_files) - 10} more files")

    # Confirm before proceeding
    print(f"\n{Colors.BOLD}Ready to merge {len(pdf_files)} PDF files!{Colors.ENDC}")

    # Merge PDFs
    success = merge_pdfs(pdf_files, output_path)

    if success:
        print(f"\n{Colors.OKGREEN}{Colors.BOLD}🎉 Mission Accomplished! 🎉{Colors.ENDC}")
        print(f"{Colors.OKGREEN}Your merged PDF is ready: {output_path.name}{Colors.ENDC}")
    else:
        print(f"\n{Colors.FAIL}{Colors.BOLD}❌ Mission Failed!{Colors.ENDC}")
        print(f"{Colors.FAIL}Some errors occurred during the merge process.{Colors.ENDC}")
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}⚠️  Operation cancelled by user{Colors.ENDC}")
        sys.exit(0)
    except Exception as e:
        print_error(f"Unexpected error: {str(e)}")
        sys.exit(1)
