from django.core.mail import EmailMessage  # ✅ CORRECT import


from django.conf import settings


def getHtmlMail(authcode, email, phone, name):
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Welcome to SmartScout</title>
    </head>
    <body style="background-color: #f3f4f6; padding: 20px; font-family: Arial, sans-serif;">
        <div style="max-width: 600px; margin: 0 auto; background: white; border-radius: 10px; padding: 20px; box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);">
            <h2 style="color: #4f46e5; text-align: center;">Welcome to SmartScout, {name}!</h2>
            <p style="color: #374151; font-size: 16px; text-align: center;">We are excited to have you on board.</p>
            
            <div style="border: 1px solid #ddd; padding: 15px; border-radius: 8px; background: #f9fafb; margin: 20px 0;">
                <p style="margin: 5px 0;"><strong>Auth Code:</strong> <span style="color: #16a34a;">{authcode}</span></p>
                <p style="margin: 5px 0;"><strong>Email:</strong> {email}</p>
                <p style="margin: 5px 0;"><strong>Phone:</strong> {phone}</p>
            </div>

            <p style="color: #374151; font-size: 14px;">If you have any questions, feel free to reach out to our support team.</p>
            
            <div style="text-align: center; margin-top: 20px;">
                <a href="https://smartscout.com" style="background-color: #4f46e5; color: white; padding: 10px 20px; border-radius: 5px; text-decoration: none; display: inline-block;">Visit SmartScout</a>
            </div>
            
            <p style="text-align: center; font-size: 12px; color: #6b7280; margin-top: 20px;">© 2025 SmartScout. All rights reserved.</p>
        </div>
    </body>
    </html>
    """

def send_manager_email(manager_email, auth_code, phone, name):
    email_body = getHtmlMail(auth_code, manager_email, phone, name)
    
    email = EmailMessage(
        subject="Successfully Add to manager",
        body=email_body,
        from_email=settings.EMAIL_HOST_USER,
        to=[manager_email],
    )
    email.content_subtype = "html"  
    email.send()