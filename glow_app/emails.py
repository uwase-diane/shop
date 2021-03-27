from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string



def send_welcome_email(name,receiver):
    subject ='WELCOME TO GLOW GIRL'
    sender = 'diane.uwase13@gmail.com'

    text_content = render_to_string('email/glowemails.txt',{"email": email})
    html_content = render_to_string('email/glowemails.html',{"email": email})
    
    msg = EmailMultiAlternatives(subject,text_content,sender,[receiver])
    msg.attach_alternative(html_content,'text/html')
    msg.send()