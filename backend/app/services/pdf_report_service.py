"""
PDF Report Generation Service

Generate professional compliance reports for cosmetic product analyses
"""

from typing import Optional
from datetime import datetime
from io import BytesIO
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

from app.models.product_compliance import ProductAnalysis


class PDFReportService:
    """Service for generating PDF compliance reports"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Set up custom paragraph styles"""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1e3a8a'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Subtitle style
        self.styles.add(ParagraphStyle(
            name='CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#4b5563'),
            spaceAfter=12,
            spaceBefore=20,
            fontName='Helvetica-Bold'
        ))
        
        # Status badge style
        self.styles.add(ParagraphStyle(
            name='StatusBadge',
            parent=self.styles['Normal'],
            fontSize=18,
            textColor=colors.white,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
    
    def generate_compliance_report(
        self,
        analysis: ProductAnalysis,
        output_path: Optional[str] = None
    ) -> BytesIO:
        """
        Generate PDF compliance report
        
        Args:
            analysis: ProductAnalysis object
            output_path: Optional file path to save PDF (if None, returns BytesIO)
            
        Returns:
            BytesIO object containing PDF data
        """
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=0.75*inch,
            bottomMargin=0.75*inch,
        )
        
        # Build document content
        story = []
        
        # Header
        story.extend(self._build_header(analysis))
        story.append(Spacer(1, 0.3*inch))
        
        # Executive Summary
        story.extend(self._build_executive_summary(analysis))
        story.append(Spacer(1, 0.3*inch))
        
        # Compliance Details
        story.extend(self._build_compliance_details(analysis))
        story.append(Spacer(1, 0.3*inch))
        
        # Findings
        if analysis.prohibited_ingredients_found or analysis.restricted_ingredients_found:
            story.extend(self._build_findings_section(analysis))
            story.append(Spacer(1, 0.3*inch))
        
        # Recommendations
        if analysis.recommendations:
            story.extend(self._build_recommendations_section(analysis))
            story.append(Spacer(1, 0.3*inch))
        
        # AI Analysis
        if analysis.ai_analysis_summary:
            story.extend(self._build_ai_analysis_section(analysis))
            story.append(Spacer(1, 0.3*inch))
        
        # Footer
        story.extend(self._build_footer(analysis))
        
        # Build PDF
        doc.build(story)
        buffer.seek(0)
        
        # Save to file if path provided
        if output_path:
            with open(output_path, 'wb') as f:
                f.write(buffer.getvalue())
            buffer.seek(0)
        
        return buffer
    
    def _build_header(self, analysis: ProductAnalysis) -> list:
        """Build report header"""
        elements = []
        
        # Title
        title = Paragraph(
            "Cosmetic Product Compliance Report",
            self.styles['CustomTitle']
        )
        elements.append(title)
        
        # Product info table
        product_data = [
            ['Product Name:', analysis.product_name],
            ['Brand:', analysis.brand_name or 'N/A'],
            ['Category:', analysis.product_category or 'N/A'],
            ['Target Market:', f"{analysis.target_country} ({analysis.regulation_type})"],
            ['Analysis Date:', analysis.created_at.strftime('%Y-%m-%d %H:%M:%S')],
        ]
        
        product_table = Table(product_data, colWidths=[2*inch, 4*inch])
        product_table.setStyle(TableStyle([
            ('FONT', (0, 0), (0, -1), 'Helvetica-Bold', 10),
            ('FONT', (1, 0), (1, -1), 'Helvetica', 10),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#4b5563')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        elements.append(product_table)
        
        return elements
    
    def _build_executive_summary(self, analysis: ProductAnalysis) -> list:
        """Build executive summary section"""
        elements = []
        
        subtitle = Paragraph("Executive Summary", self.styles['CustomSubtitle'])
        elements.append(subtitle)
        
        # Status badge color
        status_color = self._get_status_color(analysis.compliance_status.value)
        
        # Summary table
        summary_data = [
            ['Compliance Status', 'Compliance Score', 'Risk Level'],
            [
                analysis.compliance_status.value.replace('_', ' '),
                f"{analysis.compliance_score:.1f}/100",
                analysis.risk_level.value
            ]
        ]
        
        summary_table = Table(summary_data, colWidths=[2*inch, 2*inch, 2*inch])
        summary_table.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold', 11),
            ('FONT', (0, 1), (-1, 1), 'Helvetica-Bold', 14),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f3f4f6')),
            ('BACKGROUND', (0, 1), (0, 1), status_color),
            ('BACKGROUND', (1, 1), (1, 1), self._get_score_color(analysis.compliance_score)),
            ('BACKGROUND', (2, 1), (2, 1), self._get_risk_color(analysis.risk_level.value)),
            ('TEXTCOLOR', (0, 1), (-1, 1), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#d1d5db')),
            ('ROWHEIGHTS', (0, 0), (-1, -1), [25, 40]),
        ]))
        elements.append(summary_table)
        
        return elements
    
    def _build_compliance_details(self, analysis: ProductAnalysis) -> list:
        """Build compliance details section"""
        elements = []
        
        subtitle = Paragraph("Compliance Details", self.styles['CustomSubtitle'])
        elements.append(subtitle)
        
        # Warnings
        if analysis.warnings:
            warning_text = "<br/>".join([f"• {w}" for w in analysis.warnings])
            warning_para = Paragraph(warning_text, self.styles['Normal'])
            elements.append(warning_para)
        else:
            elements.append(Paragraph("✓ No compliance warnings", self.styles['Normal']))
        
        return elements
    
    def _build_findings_section(self, analysis: ProductAnalysis) -> list:
        """Build findings section"""
        elements = []
        
        subtitle = Paragraph("Ingredient Findings", self.styles['CustomSubtitle'])
        elements.append(subtitle)
        
        # Prohibited ingredients
        if analysis.prohibited_ingredients_found:
            elements.append(Paragraph(
                f"<b>⚠ Prohibited Ingredients ({len(analysis.prohibited_ingredients_found)})</b>",
                self.styles['Normal']
            ))
            elements.append(Spacer(1, 0.1*inch))
            
            for ingredient in analysis.prohibited_ingredients_found:
                ing_text = f"<b>{ingredient['ingredient_name']}</b>"
                if ingredient.get('cas_number'):
                    ing_text += f" (CAS: {ingredient['cas_number']})"
                if ingredient.get('restriction_notes'):
                    ing_text += f"<br/>{ingredient['restriction_notes']}"
                elements.append(Paragraph(ing_text, self.styles['Normal']))
                elements.append(Spacer(1, 0.05*inch))
        
        # Restricted ingredients
        if analysis.restricted_ingredients_found:
            elements.append(Spacer(1, 0.1*inch))
            elements.append(Paragraph(
                f"<b>⚡ Restricted Ingredients ({len(analysis.restricted_ingredients_found)})</b>",
                self.styles['Normal']
            ))
            elements.append(Spacer(1, 0.1*inch))
            
            for ingredient in analysis.restricted_ingredients_found:
                ing_text = f"<b>{ingredient['ingredient_name']}</b>"
                if ingredient.get('max_concentration'):
                    ing_text += f" (Max: {ingredient['max_concentration']})"
                if ingredient.get('restriction_notes'):
                    ing_text += f"<br/>{ingredient['restriction_notes']}"
                elements.append(Paragraph(ing_text, self.styles['Normal']))
                elements.append(Spacer(1, 0.05*inch))
        
        return elements
    
    def _build_recommendations_section(self, analysis: ProductAnalysis) -> list:
        """Build recommendations section"""
        elements = []
        
        subtitle = Paragraph("Recommendations", self.styles['CustomSubtitle'])
        elements.append(subtitle)
        
        for i, rec in enumerate(analysis.recommendations, 1):
            rec_para = Paragraph(f"{i}. {rec}", self.styles['Normal'])
            elements.append(rec_para)
            elements.append(Spacer(1, 0.05*inch))
        
        return elements
    
    def _build_ai_analysis_section(self, analysis: ProductAnalysis) -> list:
        """Build AI analysis section"""
        elements = []
        
        subtitle = Paragraph("AI Expert Analysis", self.styles['CustomSubtitle'])
        elements.append(subtitle)
        
        ai_para = Paragraph(analysis.ai_analysis_summary, self.styles['Normal'])
        elements.append(ai_para)
        
        if analysis.ai_model_used:
            model_para = Paragraph(
                f"<i>Powered by {analysis.ai_model_used}</i>",
                self.styles['Normal']
            )
            elements.append(Spacer(1, 0.05*inch))
            elements.append(model_para)
        
        return elements
    
    def _build_footer(self, analysis: ProductAnalysis) -> list:
        """Build report footer"""
        elements = []
        
        elements.append(Spacer(1, 0.5*inch))
        
        footer_text = f"""
        <i>
        This report was generated automatically by K-Beauty Global Leap RegTech platform.<br/>
        Analysis ID: {analysis.id}<br/>
        Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br/>
        <br/>
        Disclaimer: This analysis is provided for informational purposes only and should not be 
        considered as legal or regulatory advice. Please consult with qualified regulatory experts 
        for official compliance verification.
        </i>
        """
        
        footer_para = Paragraph(footer_text, self.styles['Normal'])
        elements.append(footer_para)
        
        return elements
    
    def _get_status_color(self, status: str) -> colors.Color:
        """Get color for compliance status"""
        color_map = {
            'COMPLIANT': colors.HexColor('#10b981'),
            'WARNING': colors.HexColor('#f59e0b'),
            'NON_COMPLIANT': colors.HexColor('#ef4444'),
            'PENDING': colors.HexColor('#6b7280'),
        }
        return color_map.get(status, colors.gray)
    
    def _get_score_color(self, score: float) -> colors.Color:
        """Get color for compliance score"""
        if score >= 90:
            return colors.HexColor('#10b981')
        elif score >= 70:
            return colors.HexColor('#f59e0b')
        elif score >= 50:
            return colors.HexColor('#f97316')
        else:
            return colors.HexColor('#ef4444')
    
    def _get_risk_color(self, risk: str) -> colors.Color:
        """Get color for risk level"""
        color_map = {
            'LOW': colors.HexColor('#10b981'),
            'MEDIUM': colors.HexColor('#f59e0b'),
            'HIGH': colors.HexColor('#f97316'),
            'CRITICAL': colors.HexColor('#ef4444'),
        }
        return color_map.get(risk, colors.gray)
