#!/usr/bin/env python3
"""
PDF Report Generator for Compliance Reports
Converts Word documents to PDF and generates PDF directly from markdown
"""

from pathlib import Path
import subprocess
import platform
import os


def convert_docx_to_pdf(docx_file: str, pdf_file: str = None) -> str:
    """
    Convert Word document to PDF

    Args:
        docx_file: Path to .docx file
        pdf_file: Output PDF path (auto-generated if not provided)

    Returns:
        Path to generated PDF file
    """
    docx_path = Path(docx_file)

    if not pdf_file:
        pdf_file = docx_path.parent / f"{docx_path.stem}.pdf"
    else:
        pdf_file = Path(pdf_file)

    # Try different methods based on platform
    system = platform.system()

    try:
        if system == "Darwin":  # macOS
            # Use LibreOffice (best option for macOS)
            _convert_using_libreoffice(docx_path, pdf_file)
        elif system == "Linux":
            # Try libreoffice
            _convert_using_libreoffice(docx_path, pdf_file)
        elif system == "Windows":
            # Try python-docx2pdf
            _convert_using_docx2pdf(docx_path, pdf_file)
        else:
            raise OSError(f"Unsupported platform: {system}")

        return str(pdf_file)

    except Exception as e:
        print(f"⚠️  Primary conversion method failed: {e}")
        print("Trying alternative method...")

        # Fallback: try python-docx2pdf if available
        try:
            _convert_using_docx2pdf(docx_path, pdf_file)
            return str(pdf_file)
        except Exception as e2:
            raise Exception(f"All conversion methods failed: {e}, {e2}")


def _convert_using_textutil(docx_path: Path, pdf_path: Path):
    """Convert using macOS textutil (doesn't preserve formatting well)"""
    # Note: textutil doesn't convert docx to PDF directly
    # This is a placeholder - better to use other methods
    raise NotImplementedError("textutil doesn't support docx to PDF conversion")


def _convert_using_libreoffice(docx_path: Path, pdf_path: Path):
    """Convert using LibreOffice (Linux/macOS/Windows)"""
    try:
        # Find LibreOffice executable
        soffice_path = 'soffice'

        # Check if soffice is in PATH
        result = subprocess.run(
            ['which', 'soffice'],
            capture_output=True,
            text=True
        )

        # If not in PATH, check standard macOS location
        if result.returncode != 0:
            macos_path = Path('/Applications/LibreOffice.app/Contents/MacOS/soffice')
            if macos_path.exists():
                soffice_path = str(macos_path)
            else:
                raise FileNotFoundError("LibreOffice not found")

        # Convert using LibreOffice headless
        output_dir = pdf_path.parent
        subprocess.run([
            soffice_path,
            '--headless',
            '--convert-to', 'pdf',
            '--outdir', str(output_dir),
            str(docx_path)
        ], check=True, capture_output=True)

        # LibreOffice creates PDF with same name as docx
        generated_pdf = output_dir / f"{docx_path.stem}.pdf"

        # Rename if needed
        if generated_pdf != pdf_path:
            generated_pdf.rename(pdf_path)

        print(f"✅ PDF created using LibreOffice")

    except subprocess.CalledProcessError as e:
        raise Exception(f"LibreOffice conversion failed: {e.stderr.decode()}")
    except FileNotFoundError:
        raise Exception("LibreOffice not installed. Install with: brew install --cask libreoffice")


def _convert_using_docx2pdf(docx_path: Path, pdf_path: Path):
    """Convert using python-docx2pdf library (Windows primarily)"""
    try:
        from docx2pdf import convert
        convert(str(docx_path), str(pdf_path))
        print(f"✅ PDF created using docx2pdf")
    except ImportError:
        raise ImportError("docx2pdf not installed. Install with: pip install docx2pdf")
    except Exception as e:
        raise Exception(f"docx2pdf conversion failed: {e}")


def generate_pdf_report(markdown_file: str = None, docx_file: str = None,
                       pdf_file: str = None, metadata: dict = None) -> str:
    """
    Generate PDF compliance report from markdown or Word document

    Args:
        markdown_file: Path to markdown file (will create docx first)
        docx_file: Path to existing .docx file
        pdf_file: Output PDF path
        metadata: Metadata for cover page (if generating from markdown)

    Returns:
        Path to generated PDF
    """
    if not docx_file and not markdown_file:
        raise ValueError("Must provide either markdown_file or docx_file")

    # If markdown provided, convert to docx first
    if markdown_file:
        from compliance_report_template import convert_markdown_to_compliance_report

        print(f"📄 Converting markdown to Word document...")
        docx_file = convert_markdown_to_compliance_report(markdown_file, metadata=metadata)
        print(f"✅ Word document created: {docx_file}")

    # Convert docx to PDF
    print(f"🔄 Converting to PDF...")
    pdf_path = convert_docx_to_pdf(docx_file, pdf_file)

    return pdf_path


if __name__ == '__main__':
    import sys
    import json

    if len(sys.argv) < 2:
        print("\n📊 PDF Report Generator")
        print("=" * 50)
        print("\nUsage:")
        print("  python report_pdf_generator.py <file> [output.pdf]")
        print("\nSupported input formats:")
        print("  - Markdown (.md) - will create Word doc first")
        print("  - Word (.docx) - direct conversion")
        print("\nExamples:")
        print("  python report_pdf_generator.py report.md report.pdf")
        print("  python report_pdf_generator.py report.docx report.pdf")
        print("\n")
        sys.exit(0)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    input_path = Path(input_file)

    try:
        if input_path.suffix == '.md':
            # Markdown to PDF
            print(f"\n🔄 Generating PDF from markdown...")
            pdf_path = generate_pdf_report(markdown_file=input_file, pdf_file=output_file)
        elif input_path.suffix == '.docx':
            # Word to PDF
            print(f"\n🔄 Converting Word document to PDF...")
            pdf_path = convert_docx_to_pdf(input_file, output_file)
        else:
            print(f"❌ Unsupported file format: {input_path.suffix}")
            print("Supported formats: .md, .docx")
            sys.exit(1)

        print(f"\n✅ PDF report created successfully!")
        print(f"📁 Location: {pdf_path}\n")

    except Exception as e:
        print(f"\n❌ Error generating PDF: {e}\n")
        sys.exit(1)
