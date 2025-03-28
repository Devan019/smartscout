def get_acceptance_email(recruitment_name, candidate_name, email, next_steps):
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Congratulations! - {recruitment_name}</title>
    </head>
    <body style="background-color: #f3f4f6; padding: 20px; font-family: Arial, sans-serif;">
        <div style="max-width: 600px; margin: 0 auto; background: white; border-radius: 10px; padding: 20px; box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);">
            <h2 style="color: #4f46e5; text-align: center;">Congratulations!</h2>
            <p style="color: #374151; font-size: 16px; text-align: center;">Dear {candidate_name},</p>
            
            <div style="border: 1px solid #ddd; padding: 15px; border-radius: 8px; background: #f9fafb; margin: 20px 0;">
                <p style="margin: 5px 0; color: #374151;">We are pleased to inform you that your application for the <strong>{recruitment_name}</strong> position has been successful!</p>
                <p style="margin: 5px 0; color: #374151;">Your skills and experience stood out among many qualified applicants, and we're excited about the prospect of you joining our team.</p>
                
                <h3 style="color: #4f46e5; margin-top: 15px;">Next Steps:</h3>
                <ul style="margin: 5px 0; padding-left: 20px; color: #374151;">
                    {''.join([f'<li>{step}</li>' for step in next_steps])}
                </ul>
            </div>

            <p style="color: #374151; font-size: 14px;">If you have any questions before the next steps, please don't hesitate to reply to this email.</p>
            
            <div style="text-align: center; margin-top: 20px;">
                <a href="https://smartscout.com/onboarding" style="background-color: #4f46e5; color: white; padding: 10px 20px; border-radius: 5px; text-decoration: none; display: inline-block;">Start Onboarding Process</a>
            </div>
            
            <p style="text-align: center; font-size: 12px; color: #6b7280; margin-top: 20px;">© 2025 SmartScout. All rights reserved.</p>
        </div>
    </body>
    </html>
    """