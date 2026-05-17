"""
PDF report generator using WeasyPrint + Jinja2 HTML templates.
Modern, presentation-ready design.
"""
import os
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import io
import base64
from src.config.settings import TEMPLATES_DIR, REPORTS_DIR, REPORT_COMPANY_NAME, REPORT_PRIMARY_COLOR
from src.utils.logger import get_logger
from src.utils.date_helpers import get_current_week_label

logger = get_logger(__name__)

class PDFReportGenerator:
    """Generate beautiful PDF reports from HTML templates."""

    def __init__(self):
        self.template_dir = TEMPLATES_DIR / 'pdf'
        self.env = Environment(loader=FileSystemLoader(self.template_dir))
        self.reports_dir = REPORTS_DIR
        self.reports_dir.mkdir(exist_ok=True)

    def _create_chart(self, data: Dict, chart_type: str = 'line') -> str:
        """Create chart and return as base64 encoded SVG."""
        fig, ax = plt.subplots(figsize=(8, 4))

        if chart_type == 'line':
            dates = data.get('dates', [])
            values = data.get('values', [])
            ax.plot(dates, values, color=REPORT_PRIMARY_COLOR, linewidth=2.5, marker='o', markersize=6)
            ax.fill_between(range(len(dates)), values, alpha=0.1, color=REPORT_PRIMARY_COLOR)

        elif chart_type == 'bar':
            labels = data.get('labels', [])
            values = data.get('values', [])
            colors = [REPORT_PRIMARY_COLOR if v >= 0 else '#ef4444' for v in values]
            ax.bar(labels, values, color=colors, width=0.6)

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.tick_params(axis='x', rotation=45)
        ax.grid(axis='y', alpha=0.3)

        plt.tight_layout()

        # Save to buffer
        buffer = io.BytesIO()
        plt.savefig(buffer, format='svg', bbox_inches='tight')
        buffer.seek(0)
        svg_data = buffer.getvalue().decode('utf-8')
        plt.close()

        return f"data:image/svg+xml;base64,{base64.b64encode(svg_data.encode()).decode()}"

    def generate_report(
        self,
        report_date: str,
        traffic_data: List[Dict],
        position_data: List[Dict],
        visibility_data: List[Dict],
        alerts: List[Dict],
        tops: List[Dict]
    ) -> str:
        """
        Generate complete PDF report.

        Returns:
            Path to generated PDF file
        """
        week_label = get_current_week_label()

        # Prepare template context
        context = {
            'company_name': REPORT_COMPANY_NAME,
            'report_date': report_date,
            'week_label': week_label,
            'primary_color': REPORT_PRIMARY_COLOR,
            'traffic_data': traffic_data,
            'position_data': position_data,
            'visibility_data': visibility_data,
            'alerts': alerts,
            'tops': tops,
            'generated_at': datetime.now().strftime('%d.%m.%Y %H:%M')
        }

        # Render HTML
        template = self.env.get_template('base.html')
        html_content = template.render(**context)

        # Generate PDF
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        pdf_path = self.reports_dir / f"seo_report_{timestamp}.pdf"

        font_config = FontConfiguration()
        HTML(string=html_content).write_pdf(
            str(pdf_path),
            font_config=font_config
        )

        logger.info(f"PDF report generated: {pdf_path}")
        return str(pdf_path)

    def generate_simple_report(self, report_date: str, summary_data: Dict) -> str:
        """Generate simplified report for testing."""
        week_label = get_current_week_label()

        context = {
            'company_name': REPORT_COMPANY_NAME,
            'report_date': report_date,
            'week_label': week_label,
            'primary_color': REPORT_PRIMARY_COLOR,
            'summary': summary_data,
            'generated_at': datetime.now().strftime('%d.%m.%Y %H:%M')
        }

        template = self.env.get_template('base.html')
        html_content = template.render(**context)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        pdf_path = self.reports_dir / f"seo_report_{timestamp}.pdf"

        font_config = FontConfiguration()
        HTML(string=html_content).write_pdf(str(pdf_path), font_config=font_config)

        logger.info(f"Simple PDF report generated: {pdf_path}")
        return str(pdf_path)


if __name__ == '__main__':
    gen = PDFReportGenerator()
    print("PDFReportGenerator initialized")
