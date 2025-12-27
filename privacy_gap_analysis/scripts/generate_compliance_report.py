#!/usr/bin/env python3
"""
Unified Compliance Report Generator
Generates professional compliance reports in multiple formats:
- Markdown (.md)
- Word (.docx) using Audit Caddie template
- PDF (.pdf)
"""

from pathlib import Path
from datetime import datetime
import argparse
from compliance_report_template import ComplianceReportTemplate, convert_markdown_to_compliance_report
from report_pdf_generator import convert_docx_to_pdf


class ComplianceReportGenerator:
    """Generate professional compliance reports in all formats"""

    def __init__(self, output_dir: str = "reports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_all_formats(self, markdown_content: str, metadata: dict,
                            base_filename: str = None) -> dict:
        """
        Generate report in all formats (markdown, Word, PDF)

        Args:
            markdown_content: Report content in markdown format
            metadata: Report metadata (company_name, title, etc.)
            base_filename: Base name for output files

        Returns:
            Dictionary with paths to generated files
        """
        if not base_filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            company = metadata.get('company_name', 'Company').replace(' ', '_')
            base_filename = f"{company}_CCPA_Compliance_Report_{timestamp}"

        files = {}

        # 1. Save Markdown
        print("\n📝 Generating Markdown report...")
        md_path = self.output_dir / f"{base_filename}.md"
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        files['markdown'] = str(md_path)
        print(f"✅ Markdown: {md_path}")

        # 2. Generate Professional Word Document
        print("\n📄 Generating professional Word document...")
        docx_path = self.output_dir / f"{base_filename}.docx"

        report = ComplianceReportTemplate.from_markdown(markdown_content, metadata)
        report.save(docx_path)
        files['docx'] = str(docx_path)
        print(f"✅ Word: {docx_path}")

        # 3. Generate PDF
        print("\n📊 Generating PDF...")
        try:
            pdf_path = self.output_dir / f"{base_filename}.pdf"
            convert_docx_to_pdf(docx_path, pdf_path)
            files['pdf'] = str(pdf_path)
            print(f"✅ PDF: {pdf_path}")
        except Exception as e:
            print(f"⚠️  PDF generation failed: {e}")
            print("   (Word document was created successfully)")
            files['pdf'] = None

        return files

    def create_report_from_analysis(self, company_name: str, analysis_data: dict,
                                   compliance_type: str = "CCPA") -> dict:
        """
        Create complete compliance report from analysis data

        Args:
            company_name: Company being analyzed
            analysis_data: Gap analysis data structure
            compliance_type: Type of compliance (CCPA, GDPR, etc.)

        Returns:
            Dictionary with paths to generated files
        """
        # Build metadata
        metadata = {
            'company_name': company_name,
            'report_title': f'{compliance_type} COMPLIANCE ASSESSMENT REPORT',
            'subtitle': f'{company_name} Privacy Policy\nCompliance Gap Analysis',
            'executive_summary': analysis_data.get('summary',
                f'The {company_name} privacy policy provides a foundational framework for data privacy. '
                f'However, several critical gaps exist concerning {compliance_type} compliance, '
                'particularly in consumer rights disclosures and data handling practices.'),
            'generated_by': f'{company_name} Privacy Policy Gap Analysis System',
            'analysis_date': datetime.now().strftime('%B %d, %Y')
        }

        # Build markdown content
        markdown_content = self._build_markdown_from_analysis(company_name, analysis_data, compliance_type)

        # Generate all formats
        return self.generate_all_formats(markdown_content, metadata)

    def _build_markdown_from_analysis(self, company_name: str, analysis_data: dict,
                                     compliance_type: str) -> str:
        """Build markdown content from analysis data structure"""

        md = []

        # Title
        md.append(f"# {company_name} {compliance_type} Compliance Report\n")

        # Executive Summary
        md.append("## EXECUTIVE SUMMARY\n")
        md.append(analysis_data.get('summary', 'Analysis summary not provided.'))
        md.append("\n")

        # Purpose
        md.append("### Purpose of this Report\n")
        md.append(f"The primary objective of this report is to identify specific gaps in {company_name}'s "
                 f"privacy policy when measured against the requirements of the {compliance_type}.")
        md.append("\n")

        # Scope
        md.append("### Scope of the Analysis\n")
        md.append(f"The analysis covers critical domains of {compliance_type}, including consumer rights "
                 "disclosures, data collection and retention policies, third-party data sharing, "
                 "and procedures for exercising privacy rights.")
        md.append("\n")

        # Assessment Methodology
        md.append("## ASSESSMENT METHODOLOGY\n")
        md.append("This analysis evaluates the privacy policy against specific compliance requirements, "
                 "identifying gaps and providing remediation recommendations.")
        md.append("\n")

        # Gap Analysis
        if 'gaps' in analysis_data:
            md.append("## DETAILED GAP ANALYSIS\n")
            for gap in analysis_data['gaps']:
                md.append(f"### {gap.get('title', 'Gap')}\n")
                md.append(gap.get('description', ''))
                if gap.get('priority'):
                    md.append(f"\n**Priority:** {gap['priority']}")
                md.append("\n")

        # Recommendations
        if 'recommendations' in analysis_data:
            md.append("## RECOMMENDATIONS\n")
            for rec in analysis_data['recommendations']:
                md.append(f"- {rec}")
            md.append("\n")

        # Priority Actions
        if 'priority_actions' in analysis_data:
            md.append("## PRIORITY ACTIONS\n")
            for action in analysis_data['priority_actions']:
                md.append(f"- {action}")
            md.append("\n")

        return '\n'.join(md)


def main():
    """Command-line interface for report generation"""
    parser = argparse.ArgumentParser(
        description='Generate professional compliance reports in multiple formats'
    )

    parser.add_argument('--markdown', '-m', help='Input markdown file')
    parser.add_argument('--output-dir', '-o', default='reports', help='Output directory')
    parser.add_argument('--company', '-c', help='Company name')
    parser.add_argument('--format', '-f', choices=['all', 'docx', 'pdf', 'md'],
                       default='all', help='Output format')

    args = parser.parse_args()

    generator = ComplianceReportGenerator(args.output_dir)

    if args.markdown:
        # Read markdown file
        with open(args.markdown, 'r', encoding='utf-8') as f:
            markdown_content = f.read()

        # Extract company name from file or use provided
        company_name = args.company or Path(args.markdown).stem.split('_')[0]

        metadata = {
            'company_name': company_name,
            'report_title': 'COMPLIANCE ASSESSMENT REPORT',
            'subtitle': f'{company_name} Privacy Policy\nCompliance Gap Analysis',
            'executive_summary': 'Comprehensive compliance gap analysis report.',
            'generated_by': 'Privacy Policy Gap Analysis System',
            'analysis_date': datetime.now().strftime('%B %d, %Y')
        }

        print(f"\n{'='*60}")
        print(f"  Generating {company_name} Compliance Report")
        print(f"{'='*60}")

        files = generator.generate_all_formats(markdown_content, metadata)

        print(f"\n{'='*60}")
        print("✅ Report Generation Complete!")
        print(f"{'='*60}")
        print("\n📁 Generated Files:")
        for format_type, filepath in files.items():
            if filepath:
                print(f"  {format_type.upper():10s} {filepath}")

    else:
        print("\n❌ Error: Please provide --markdown input file")
        parser.print_help()


if __name__ == '__main__':
    main()
