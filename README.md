# PDF Merger Pro 📄✨

A powerful and user-friendly command-line tool for merging PDF files with style! Perfect for combining course materials, documents, or any collection of PDFs.

## 🚀 Features

- **🎯 Smart Merging**: Automatically finds and merges PDF files from any folder
- **📁 Recursive Search**: Scan subfolders with the `--recursive` flag
- **🎨 Beautiful CLI**: Progress bars, emojis, and color-coded messages
- **⚡ Fast Processing**: Efficient PDF handling with modern libraries
- **🔧 Flexible Options**: Custom output names and destination folders
- **📊 Detailed Stats**: File count, page count, and size information
- **🛡️ Error Handling**: Robust error handling and user-friendly messages

## 📦 Installation

1. **Clone the repository:**
   ```bash
   git clone git@github.com:ErikKopcha/pdf-merger.git
   cd pdf-merger
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## 🎮 Usage

### Basic Usage
```bash
python pdf_merger.py /path/to/folder
```

### Advanced Usage
```bash
# Merge PDFs with custom output name
python pdf_merger.py /path/to/folder --output "My_Merged_Document"

# Recursive search in subfolders
python pdf_merger.py /path/to/folder --recursive

# Custom destination folder
python pdf_merger.py /path/to/folder --destination /path/to/output

# Combine all options
python pdf_merger.py /path/to/folder --output "Complete_Course" --recursive --destination ~/Documents
```

### Command Line Arguments

| Argument | Description | Example |
|----------|-------------|---------|
| `folder_path` | Path to folder containing PDFs | `/Users/john/Documents` |
| `--output` | Custom name for output PDF | `--output "My_Document"` |
| `--recursive` | Search in subfolders | `--recursive` |
| `--destination` | Output folder path | `--destination ~/Downloads` |
| `--help` | Show help message | `--help` |

## 📋 Examples

### Example 1: Merge Course Materials
```bash
python pdf_merger.py "Python Course" --output "Python_Complete" --recursive
```
**Result:** All PDFs from "Python Course" folder and subfolders merged into "Python_Complete.pdf"

### Example 2: Merge Single Folder
```bash
python pdf_merger.py "Topic 1"
```
**Result:** All PDFs from "Topic 1" folder merged into "Topic 1.pdf"

### Example 3: Custom Destination
```bash
python pdf_merger.py "Documents" --destination ~/Desktop --output "All_Docs"
```
**Result:** Merged PDF saved as "All_Docs.pdf" on Desktop

## 🔧 Requirements

- Python 3.7+
- pypdf >= 4.0.0
- tqdm >= 4.65.0

## 📁 Project Structure

```
pdf-merger/
├── pdf_merger.py    # Main script
├── requirements.txt     # Dependencies
├── README.md           # Documentation
└── .gitignore         # Git ignore rules
```

## 🎨 Features in Detail

### Smart File Sorting
- Automatically sorts files alphabetically
- Prioritizes "Introduction" and "Conclusion" files
- Handles Ukrainian and English file names

### Progress Tracking
- Real-time progress bars during merging
- File-by-file processing updates
- Final statistics summary

### Error Handling
- Graceful handling of corrupted PDFs
- Clear error messages
- Continues processing even if some files fail

### Output Information
- 📄 Total files processed
- 📖 Total pages in merged PDF
- 💾 Final file size
- ✅ Success confirmation

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🐛 Issues & Support

If you encounter any issues or have questions:
1. Check the [Issues](https://github.com/ErikKopcha/pdf-merger/issues) page
2. Create a new issue with detailed description
3. Include error messages and system information

## 🌟 Acknowledgments

- Built with ❤️ for efficient PDF management
- Powered by [pypdf](https://github.com/py-pdf/pypdf) library
- CLI enhanced with [tqdm](https://github.com/tqdm/tqdm) progress bars

---

**Happy PDF Merging! 🎉**
