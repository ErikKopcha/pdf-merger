"""CLI application entry point."""

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

from cli.parser import build_parser
from config.settings import MergeSettings
from core.merger import PdfMergerService
from core.orchestrator import MergeOrchestrator
from core.scanner import PdfScanner
from utils.console import ConsoleMessenger


@dataclass
class PdfMergerApp:
    """Orchestrates CLI -> Core integration."""

    messenger: ConsoleMessenger = field(default_factory=ConsoleMessenger)

    def run(self, argv: Optional[List[str]] = None) -> int:
        parser = build_parser()
        args = parser.parse_args(argv)

        print(
            self.messenger.banner(
                """
╔══════════════════════════════════════════════════════════════╗
║                    🚀 PDF Merger Pro 🚀                     ║
║              Advanced PDF Merging Tool v2.0                 ║
║                                                            ║
║  Merge PDFs like a pro with style and efficiency!           ║
╚══════════════════════════════════════════════════════════════╝
""".rstrip()
            )
        )

        settings = self._build_settings(
            args.folder_path, args.recursive, args.output, args.destination
        )
        orchestrator = MergeOrchestrator(
            scanner=PdfScanner(),
            merger=PdfMergerService(self.messenger),
            messenger=self.messenger,
        )

        try:
            outcome = orchestrator.execute(settings)
        except (FileNotFoundError, NotADirectoryError) as exc:
            print(self.messenger.error(str(exc)))
            return 1
        except RuntimeError as exc:
            print(self.messenger.error(str(exc)))
            return 1
        except KeyboardInterrupt:
            print(self.messenger.warning("Operation cancelled by user"))
            return 1
        except Exception as exc:  # pragma: no cover - safety net
            print(self.messenger.error(f"Unexpected error: {exc}"))
            return 1

        if outcome is None:
            return 0

        print(
            self.messenger.success(f"Successfully created: {outcome.output_path.name}")
        )
        print(self.messenger.info(f"Total pages: {outcome.total_pages}"))
        print(self.messenger.info(f"File size: {outcome.file_size_mb:.2f} MB"))
        print(
            self.messenger.success(
                f"🎉 Mission Accomplished! Your merged PDF is ready: {outcome.output_path}"
            )
        )
        return 0

    def _build_settings(
        self,
        folder_path: str,
        recursive: bool,
        output: Optional[str],
        destination: Optional[str],
    ) -> MergeSettings:
        return MergeSettings(
            folder_path=Path(folder_path).expanduser().resolve(),
            recursive=recursive,
            output_name=output,
            destination=Path(destination).expanduser().resolve()
            if destination
            else None,
        )


def main(argv: Optional[List[str]] = None) -> int:
    app = PdfMergerApp()
    return app.run(argv)


if __name__ == "__main__":  # pragma: no cover - CLI hook
    sys.exit(main())
