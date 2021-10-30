import smtplib, ssl

port = 465  # For SSL

# Create a secure SSL context
context = ssl.create_default_context()
server = smtplib.SMTP_SSL("smtp.gmail.com", port, context=context)
adminEmail = "bootlegebay@gmail.com"
server.login(adminEmail, "bootleg1234!") # Plaintext :)

def SendEmail(configuration):
    message = f"Subject: {configuration['subject']}\n\n {configuration['body']}"
    server.sendmail(adminEmail, configuration["recipient"], message)
    return "OK"