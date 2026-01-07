#!/usr/bin/env python3
"""
Professional Compliance Report Template Generator
Based on Audit Caddie CCPA Compliance Report format
Generates Word (.docx) and PDF reports from markdown or structured data
"""

from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from datetime import datetime
import re
from pathlib import Path


class ComplianceReportTemplate:
    """Professional compliance report generator with template-based formatting"""

    # Color scheme from Audit Caddie template
    PRIMARY_COLOR = RGBColor(0, 51, 102)      # Dark blue
    SECONDARY_COLOR = RGBColor(0, 112, 192)   # Blue
    ACCENT_COLOR = RGBColor(68, 114, 196)     # Light blue
    TEXT_COLOR = RGBColor(0, 0, 0)            # Black

    def __init__(self):
        self.doc = Document()
        self._setup_styles()

    def _setup_styles(self):
        """Configure professional document styles matching Audit Caddie template"""

        # Title style (cover page company name)
        title_style = self.doc.styles['Title']
        title_font = title_style.font
        title_font.name = 'Calibri'
        title_font.size = Pt(28)
        title_font.bold = True
        title_font.color.rgb = self.PRIMARY_COLOR

        # Heading 1 style (main sections - EXECUTIVE SUMMARY, etc.)
        h1_style = self.doc.styles['Heading 1']
        h1_font = h1_style.font
        h1_font.name = 'Calibri'
        h1_font.size = Pt(18)
        h1_font.bold = True
        h1_font.color.rgb = self.SECONDARY_COLOR
        h1_format = h1_style.paragraph_format
        h1_format.space_before = Pt(18)
        h1_format.space_after = Pt(12)

        # Heading 2 style (subsections)
        h2_style = self.doc.styles['Heading 2']
        h2_font = h2_style.font
        h2_font.name = 'Calibri'
        h2_font.size = Pt(14)
        h2_font.bold = True
        h2_font.color.rgb = self.ACCENT_COLOR
        h2_format = h2_style.paragraph_format
        h2_format.space_before = Pt(12)
        h2_format.space_after = Pt(6)

        # Heading 3 style (metadata labels)
        h3_style = self.doc.styles['Heading 3']
        h3_font = h3_style.font
        h3_font.name = 'Calibri'
        h3_font.size = Pt(12)
        h3_font.bold = True
        h3_font.color.rgb = self.PRIMARY_COLOR

        # Normal/Body text
        normal_style = self.doc.styles['Normal']
        normal_font = normal_style.font
        normal_font.name = 'Calibri'
        normal_font.size = Pt(11)
        normal_font.color.rgb = self.TEXT_COLOR

        # Body Text style (for summary/intro text)
        try:
            body_style = self.doc.styles['Body Text']
        except KeyError:
            body_style = self.doc.styles.add_style('Body Text', WD_STYLE_TYPE.PARAGRAPH)

        body_font = body_style.font
        body_font.name = 'Calibri'
        body_font.size = Pt(11)
        body_format = body_style.paragraph_format
        body_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE

    def add_cover_page(self, company_name: str, report_title: str, subtitle: str,
                       executive_summary: str, generated_by: str = None,
                       analysis_date: str = None):
        """
        Add professional cover page matching Audit Caddie template

        Args:
            company_name: Company name for header
            report_title: Main report title (e.g., "COMPLIANCE ASSESSMENT REPORT")
            subtitle: Report subtitle (e.g., "Audit Caddie Privacy Policy")
            executive_summary: Brief summary for cover page
            generated_by: System/analyst name
            analysis_date: Date of analysis
        """
        # Company name header
        p = self.doc.add_paragraph()
        run = p.add_run(company_name)
        run.font.name = 'Calibri'
        run.font.size = Pt(16)
        run.font.bold = True
        run.font.color.rgb = self.PRIMARY_COLOR
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT

        # Add spacing
        self.doc.add_paragraph()

        # Compliance level indicator (20/25 style)
        p = self.doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run("20\nCOMPLIANCE\t25")
        run.font.name = 'Calibri'
        run.font.size = Pt(14)
        run.font.color.rgb = self.TEXT_COLOR

        # Main title
        p = self.doc.add_paragraph()
        run = p.add_run(report_title)
        run.font.name = 'Calibri'
        run.font.size = Pt(24)
        run.font.bold = True
        run.font.color.rgb = self.PRIMARY_COLOR
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(12)

        # Subtitle
        p = self.doc.add_paragraph(subtitle)
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.runs[0].font.size = Pt(14)
        p.runs[0].font.color.rgb = self.TEXT_COLOR

        # Add spacing
        for _ in range(6):
            self.doc.add_paragraph()

        # Executive summary box
        p = self.doc.add_paragraph()
        run = p.add_run(executive_summary)
        run.font.name = 'Calibri'
        run.font.size = Pt(11)
        p.paragraph_format.line_spacing = 1.5
        p.style = 'Body Text'

        # Add spacing
        for _ in range(2):
            self.doc.add_paragraph()

        # Metadata section
        if generated_by:
            self.doc.add_heading('Report Generated By', level=3)
            p = self.doc.add_paragraph(generated_by)
            p.style = 'Body Text'
            p.runs[0].font.size = Pt(11)

        if analysis_date:
            self.doc.add_heading('Analysis Date', level=3)
            p = self.doc.add_paragraph(analysis_date)
            p.style = 'Body Text'
            p.runs[0].font.size = Pt(11)

        # Page break before content
        self.doc.add_page_break()

    def add_section_header(self, title: str):
        """Add a major section header (EXECUTIVE SUMMARY style)"""
        self.doc.add_heading(title.upper(), level=1)

    def add_subsection(self, title: str, content: str = None):
        """Add a subsection with optional content"""
        self.doc.add_heading(title, level=2)
        if content:
            p = self.doc.add_paragraph(content)
            p.style = 'Body Text'

    def add_paragraph(self, text: str, bold: bool = False):
        """Add a formatted paragraph"""
        p = self.doc.add_paragraph()
        run = p.add_run(text)
        if bold:
            run.bold = True
        p.style = 'Body Text'

    def add_bullet_list(self, items: list):
        """Add a bulleted list"""
        for item in items:
            p = self.doc.add_paragraph(item, style='List Bullet')
            p.paragraph_format.left_indent = Inches(0.25)

    def add_gap_finding(self, title: str, description: str, priority: str = None):
        """Add a compliance gap finding with formatting"""
        # Finding title
        self.doc.add_heading(title, level=2)

        # Description
        p = self.doc.add_paragraph(description)
        p.style = 'Body Text'

        # Priority indicator if provided
        if priority:
            p = self.doc.add_paragraph()
            run = p.add_run(f"Priority: {priority}")
            run.bold = True
            if priority.lower() in ['high', 'critical']:
                run.font.color.rgb = RGBColor(192, 0, 0)  # Red
            elif priority.lower() == 'medium':
                run.font.color.rgb = RGBColor(192, 128, 0)  # Orange
            else:
                run.font.color.rgb = RGBColor(0, 128, 0)  # Green

        self.doc.add_paragraph()  # Spacing

    def add_table_of_contents(self, sections: list):
        """Add a simple table of contents"""
        self.doc.add_heading('Table of Contents', level=1)
        for section in sections:
            indent = "   " * (section.get('level', 0))
            p = self.doc.add_paragraph(f"{indent}{section['title']}")
            p.paragraph_format.left_indent = Inches(0.25 * section.get('level', 0))

    def save(self, filepath: str):
        """Save the document"""
        self.doc.save(filepath)
        return filepath

    @classmethod
    def from_markdown(cls, markdown_content: str, metadata: dict = None):
        """
        Create a compliance report from markdown content

        Args:
            markdown_content: Markdown formatted content
            metadata: Dictionary with report metadata (company_name, title, etc.)

        Returns:
            ComplianceReportTemplate instance
        """
        template = cls()

        # Extract or use provided metadata
        if not metadata:
            metadata = cls._extract_metadata_from_markdown(markdown_content)

        # Add cover page if metadata exists
        if metadata.get('company_name'):
            template.add_cover_page(
                company_name=metadata.get('company_name', 'Company'),
                report_title=metadata.get('report_title', 'COMPLIANCE ASSESSMENT REPORT'),
                subtitle=metadata.get('subtitle', 'Privacy Policy Gap Analysis'),
                executive_summary=metadata.get('executive_summary', ''),
                generated_by=metadata.get('generated_by', 'Compliance Analysis System'),
                analysis_date=metadata.get('analysis_date', datetime.now().strftime('%B %d, %Y'))
            )

        # Parse markdown content
        cls._parse_markdown_content(markdown_content, template)

        return template

    @staticmethod
    def _extract_metadata_from_markdown(markdown: str) -> dict:
        """Extract metadata from markdown frontmatter or content"""
        metadata = {}

        # Try to extract from first heading
        lines = markdown.split('\n')
        for line in lines[:10]:
            if line.startswith('# '):
                metadata['company_name'] = line[2:].strip()
                break

        return metadata

    @staticmethod
    def _parse_markdown_content(markdown: str, template):
        """Parse markdown and add to template"""
        lines = markdown.split('\n')
        in_list = False
        list_items = []

        for line in lines:
            line = line.rstrip()

            if not line:
                if in_list:
                    template.add_bullet_list(list_items)
                    list_items = []
                    in_list = False
                continue

            # Main heading (# )
            if line.startswith('# ') and not line.startswith('## '):
                if in_list:
                    template.add_bullet_list(list_items)
                    list_items = []
                    in_list = False
                template.add_section_header(line[2:].strip())
                continue

            # Heading 1 (##)
            if line.startswith('## ') and not line.startswith('### '):
                if in_list:
                    template.add_bullet_list(list_items)
                    list_items = []
                    in_list = False
                template.add_subsection(line[3:].strip())
                continue

            # List item
            if line.startswith('- '):
                in_list = True
                list_items.append(line[2:].strip())
                continue

            # Regular paragraph
            if in_list:
                template.add_bullet_list(list_items)
                list_items = []
                in_list = False

            template.add_paragraph(line)

        # Add remaining list items
        if in_list and list_items:
            template.add_bullet_list(list_items)


def convert_markdown_to_compliance_report(markdown_file: str, output_file: str = None,
                                          metadata: dict = None) -> str:
    """
    Convert markdown file to professional compliance report (Word)

    Args:
        markdown_file: Path to markdown file
        output_file: Output .docx path (auto-generated if not provided)
        metadata: Optional metadata dict for cover page

    Returns:
        Path to generated .docx file
    """
    # Read markdown
    with open(markdown_file, 'r', encoding='utf-8') as f:
        markdown_content = f.read()

    # Generate output filename
    if not output_file:
        base_name = Path(markdown_file).stem
        output_file = Path(markdown_file).parent / f"{base_name}_Professional.docx"

    # Create report from template
    report = ComplianceReportTemplate.from_markdown(markdown_content, metadata)

    # Save
    report.save(output_file)

    return str(output_file)


if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1:
        markdown_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else None

        print(f"\n Converting {markdown_file} to professional compliance report...")
        docx_path = convert_markdown_to_compliance_report(markdown_file, output_file)
        print(f" Professional report created: {docx_path}\n")
    else:
        print("\n Compliance Report Template Generator")
        print("=" * 50)
        print("\nUsage: python compliance_report_template.py <markdown_file> [output_file]")
        print("\nExample:")
        print("  python compliance_report_template.py report.md report.docx")
        print("\nThis creates a professional compliance report using the")
        print("Audit Caddie CCPA Compliance Report template.\n")
