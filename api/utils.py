# utils.py
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from django.http import HttpResponse
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
import os
from django.conf import settings

def generate_teacher_pdf(teacher, assignments):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Create custom style for title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=30,
        alignment=1  # Center aligned
    )
    
    # Create story (content)
    story = []
    
    # Add title
    story.append(Paragraph(f"Teacher Report: {teacher.name}", title_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Add assignments data
    for assignment in assignments:
        # Assignment title
        story.append(Paragraph(f"Assignment: {assignment.title}", styles['Heading2']))
        
        # Student info
        story.append(Paragraph(f"Student: {assignment.assigned_to.name}", styles['Normal']))
        
        # Solution (if exists)
        if hasattr(assignment, 'submission'):
            story.append(Paragraph(f"Solution: {assignment.submission.solution}", styles['Normal']))
        else:
            story.append(Paragraph("Solution: Not submitted", styles['Normal']))
        
        # Grade (if exists)
        if hasattr(assignment, 'grade'):
            story.append(Paragraph(f"Grade: {assignment.grade.grades}", styles['Normal']))
        else:
            story.append(Paragraph("Grade: Not graded", styles['Normal']))
        
        story.append(Spacer(1, 0.2*inch))
    
    # Build PDF
    doc.build(story)
    
    # Get PDF content
    pdf = buffer.getvalue()
    buffer.close()
    
    return pdf

def generate_student_pdf(student, assignments):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Create custom style for title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=30,
        alignment=1  # Center aligned
    )
    
    # Create story (content)
    story = []
    
    # Add title
    story.append(Paragraph(f"Student Report: {student.name}", title_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Add assignments data
    for assignment in assignments:
        # Assignment title
        story.append(Paragraph(f"Assignment: {assignment.title}", styles['Heading2']))
        
        # Solution (if exists)
        if hasattr(assignment, 'submission'):
            story.append(Paragraph(f"Solution: {assignment.submission.solution}", styles['Normal']))
        else:
            story.append(Paragraph("Solution: Not submitted", styles['Normal']))
        
        # Grade (if exists)
        if hasattr(assignment, 'grade'):
            story.append(Paragraph(f"Grade: {assignment.grade.grades}", styles['Normal']))
        else:
            story.append(Paragraph("Grade: Not graded", styles['Normal']))
        
        story.append(Spacer(1, 0.2*inch))
    
    # Build PDF
    doc.build(story)
    
    # Get PDF content
    pdf = buffer.getvalue()
    buffer.close()
    
    return pdf