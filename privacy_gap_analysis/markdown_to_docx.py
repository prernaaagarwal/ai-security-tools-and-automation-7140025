#!/usr/bin/env python3
"""
Markdown to Word Document Converter
Converts markdown gap analysis reports to professional Word documents (.docx)
"""

import re
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE
import os


def convert_markdown_to_docx(markdown_file_path: str, output_file_path: str = None):
    """
    Convert a markdown file to a formatted Word document.

    Args:
        markdown_file_path: Path to the markdown file
        output_file_path: Optional output path for .docx file (auto-generated if not provided)

    Returns:
        Path to the generated .docx file
    """

    # Generate output filename if not provided
    if not output_file_path:
        base_name = os.path.splitext(markdown_file_path)[0]
        output_file_path = f"{base_name}.docx"

    # Read the markdown file
    with open(markdown_file_path, 'r', encoding='utf-8') as f:
        markdown_content = f.read()

    # Create a new Word document
    doc = Document()

    # Set up styles
    _setup_document_styles(doc)

    # Parse and convert markdown to Word
    _parse_markdown_to_docx(markdown_content, doc)

    # Save the document
    doc.save(output_file_path)

    return output_file_path


def _setup_document_styles(doc):
    """Set up custom styles for the document"""

    # Title style
    title_style = doc.styles['Title']
    title_font = title_style.font
    title_font.name = 'Calibri'
    title_font.size = Pt(24)
    title_font.bold = True
    title_font.color.rgb = RGBColor(0, 51, 102)  # Dark blue

    # Heading 1 style
    h1_style = doc.styles['Heading 1']
    h1_font = h1_style.font
    h1_font.name = 'Calibri'
    h1_font.size = Pt(18)
    h1_font.bold = True
    h1_font.color.rgb = RGBColor(0, 112, 192)  # Blue

    # Heading 2 style
    h2_style = doc.styles['Heading 2']
    h2_font = h2_style.font
    h2_font.name = 'Calibri'
    h2_font.size = Pt(14)
    h2_font.bold = True
    h2_font.color.rgb = RGBColor(68, 114, 196)  # Light blue

    # Normal style
    normal_style = doc.styles['Normal']
    normal_font = normal_style.font
    normal_font.name = 'Calibri'
    normal_font.size = Pt(11)


def _parse_markdown_to_docx(markdown_content, doc):
    """Parse markdown content and add it to the Word document"""

    lines = markdown_content.split('\n')
    i = 0
    in_list = False
    list_items = []

    while i < len(lines):
        line = lines[i].rstrip()

        # Skip empty lines unless we're in a list
        if not line:
            if in_list:
                _add_list_to_doc(list_items, doc)
                list_items = []
                in_list = False
            i += 1
            continue

        # Main title (# )
        if line.startswith('# ') and not line.startswith('## '):
            if in_list:
                _add_list_to_doc(list_items, doc)
                list_items = []
                in_list = False
            title = line[2:].strip()
            doc.add_heading(title, level=0)
            i += 1
            continue

        # Heading 1 (##)
        if line.startswith('## ') and not line.startswith('### '):
            if in_list:
                _add_list_to_doc(list_items, doc)
                list_items = []
                in_list = False
            heading = line[3:].strip()
            doc.add_heading(heading, level=1)
            i += 1
            continue

        # Heading 2 (###)
        if line.startswith('### '):
            if in_list:
                _add_list_to_doc(list_items, doc)
                list_items = []
                in_list = False
            heading = line[4:].strip()
            doc.add_heading(heading, level=2)
            i += 1
            continue

        # Horizontal rule (---)
        if line.startswith('---'):
            if in_list:
                _add_list_to_doc(list_items, doc)
                list_items = []
                in_list = False
            doc.add_paragraph('_' * 50)
            i += 1
            continue

        # Bold text (**text**)
        if line.startswith('**') and line.endswith('**'):
            if in_list:
                _add_list_to_doc(list_items, doc)
                list_items = []
                in_list = False
            text = line[2:-2]
            p = doc.add_paragraph()
            run = p.add_run(text)
            run.bold = True
            i += 1
            continue

        # List item (-)
        if line.startswith('- '):
            in_list = True
            item_text = line[2:].strip()
            list_items.append(item_text)
            i += 1
            continue

        # Regular paragraph
        if in_list:
            _add_list_to_doc(list_items, doc)
            list_items = []
            in_list = False

        # Format text with bold and other markdown
        formatted_text = _format_inline_markdown(line)
        _add_formatted_paragraph(formatted_text, doc)
        i += 1

    # Add any remaining list items
    if in_list and list_items:
        _add_list_to_doc(list_items, doc)


def _format_inline_markdown(text):
    """Format inline markdown like **bold** """
    return text


def _add_formatted_paragraph(text, doc):
    """Add a paragraph with inline formatting"""
    p = doc.add_paragraph()

    # Split by ** for bold text
    parts = re.split(r'(\*\*.*?\*\*)', text)

    for part in parts:
        if part.startswith('**') and part.endswith('**'):
            # Bold text
            run = p.add_run(part[2:-2])
            run.bold = True
        else:
            # Normal text
            p.add_run(part)


def _add_list_to_doc(list_items, doc):
    """Add a list of items to the document"""
    for item in list_items:
        # Check if item contains sub-bullets or formatting
        if '**' in item:
            p = doc.add_paragraph(style='List Bullet')
            # Split by ** for bold text
            parts = re.split(r'(\*\*.*?\*\*)', item)
            for part in parts:
                if part.startswith('**') and part.endswith('**'):
                    run = p.add_run(part[2:-2])
                    run.bold = True
                else:
                    p.add_run(part)
        else:
            doc.add_paragraph(item, style='List Bullet')


if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1:
        markdown_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else None

        print(f"\nConverting {markdown_file} to Word document...")
        docx_path = convert_markdown_to_docx(markdown_file, output_file)
        print(f"✓ Word document created: {docx_path}\n")
    else:
        print("\nUsage: python markdown_to_docx.py <markdown_file> [output_file]")
        print("Example: python markdown_to_docx.py report.md report.docx\n")
