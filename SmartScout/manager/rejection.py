def get_rejection_email(recruitment_name, candidate_name, email):
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Application Update - {recruitment_name}</title>
    </head>
    <body style="background-color: #f3f4f6; padding: 20px; font-family: Arial, sans-serif;">
        <div style="max-width: 600px; margin: 0 auto; background: white; border-radius: 10px; padding: 20px; box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);">
            <h2 style="color: #4f46e5; text-align: center;">Application Update</h2>
            <p style="color: #374151; font-size: 16px; text-align: center;">Dear {candidate_name},</p>
            
            <div style="border: 1px solid #ddd; padding: 15px; border-radius: 8px; background: #f9fafb; margin: 20px 0;">
                <p style="margin: 5px 0; color: #374151;">Thank you for applying for the <strong>{recruitment_name}</strong> position.</p>
                <p style="margin: 5px 0; color: #374151;">After careful consideration, we regret to inform you that we have decided to move forward with other candidates whose qualifications more closely match our current needs.</p>
                <p style="margin: 5px 0; color: #374151;">This decision was not easy as we were impressed with your skills and experience.</p>
            </div>

            <p style="color: #374151; font-size: 14px;">We appreciate the time and effort you invested in your application and encourage you to apply for future opportunities that may be a better fit.</p>
            
            <div style="text-align: center; margin-top: 20px;">
                <a href="https://smartscout.com/careers" style="background-color: #4f46e5; color: white; padding: 10px 20px; border-radius: 5px; text-decoration: none; display: inline-block;">View Other Opportunities</a>
            </div>
            
            <p style="text-align: center; font-size: 12px; color: #6b7280; margin-top: 20px;">© 2025 SmartScout. All rights reserved.</p>
        </div>
    </body>
    </html>
    """