from celery import shared_task
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from django.conf import settings
from .models import Assingment
from .utils import generate_student_pdf  # Your PDF generation function


@shared_task
def generate_student_report_task(user_id):
    User = get_user_model()
    
    try:
        user = User.objects.get(id=user_id)
        
        # Get all assignments assigned to this student
        assignments = Assingment.objects.filter(
            assigned_to=user
        ).prefetch_related('submission', 'grade')
        
        # Generate PDF
        pdf_content = generate_student_pdf(user, assignments)
        
        return pdf_content
    except Exception as e:
        raise e

@shared_task
def send_student_report_email_task(user_id, pdf_content):
    User = get_user_model()
    
    try:
        user = User.objects.get(id=user_id)
        
        subject = 'Pdf Report'
        html = render_to_string('api/email.html', {'user_full_name': user.name})
        from_email = 'admin@example.com'
        to = [user.email] 
        
        email = EmailMessage(
            subject=subject, 
            body=html, 
            from_email=from_email, 
            to=to
        )
        email.content_subtype = "html"
        email.attach('report.pdf', pdf_content, 'application/pdf')
        email.send()
        
        return f"Email sent successfully to {user.email}"
    except Exception as e:
        raise e

@shared_task
def generate_and_send_report_task(user_id):
    """Combined task that generates report and sends email"""
    try:
            # Generate the report
        pdf_content = generate_student_report_task(user_id)
            
            # Send the email with the report
        result = send_student_report_email_task(user_id, pdf_content)
        
        return result
    except Exception as e:
        raise e