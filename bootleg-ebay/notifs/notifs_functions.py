import smtplib, ssl
import poplib
import email
import getpass
import json

port = 465  # For SSL




def _create_connection():
    # Create a secure SSL context
    context = ssl.create_default_context()
    server = smtplib.SMTP_SSL("smtp.gmail.com", port, context=context)
    adminEmail = "bootlegebay@gmail.com"
    server.login(adminEmail, "bootleg1234!") # Plaintext :)

    return server, adminEmail

def send_email(configuration):
    """
    Configuration has attributes subject, body, and recipient.
    """
    server, adminEmail = _create_connection()
    message = f"Subject: {configuration['subject']}\n\n {configuration['body']}"
    server.sendmail(adminEmail, configuration["recipient"], message)
    server.quit()
    return "OK"


def watchlist_notification(recipient, item_id):
    """
    This sends an email to the specified recipient that
    the item they want is now available.
    """
    body = "An item on your watchlist is now available! View it here at: http://localhost:3000/items/%s" % item_id
    subject = "Watchlist item available!"
    configuration = {"body": body, "subject": subject, "recipient": recipient}
    return send_email(configuration)

def alert_seller_bid(recipient, item_id):
    """
    This sends an email to the seller when their item has been bid on.
    """
    body = "Congratulations. Your item has been bid on. View it here at: http://localhost:3000/items/%s" % item_id
    subject = "Your item has been bid on!"
    configuration = {"body": body, "subject": subject, "recipient": recipient}
    return send_email(configuration)

def alert_buyer_bid(recipient, item_id):
    """
    This sends an email to the buyer when an item they previously bid on
    has been outbid.
    """
    body = "Your bid has been outbid! Place a higher bid here at: http:localhost:3000/items/%s" % item_id
    subject = "You have been outbid."
    configuration = {"body": body, "subject": subject, "recipient": recipient}
    return send_email(configuration)

def alert_before(recipient, item_id, time_left):
    """
    Alerts seller or buyer of the time left in an auction

    time_left will take the values 'One Day', 'One Hour'
    """
    body = "There is only %s left in your auction. View it here: http:localhost:3000/items/%s" % (time_left, item_id)
    subject = time_left + " left in auction."
    configuration = {"body": body, "subject": subject, "recipient": recipient}
    return send_email(configuration)

def fetch_messages():
    """
    This gets the emails from the admin mailbox
    """
    non_read = ["The Google team <google-noreply@google.com>"]
    pop_conn = poplib.POP3_SSL('pop.gmail.com')
    pop_conn.user('bootlegebay@gmail.com')
    pop_conn.pass_("bootleg1234!")

    num_messages = len(pop_conn.list()[1])
    print(num_messages)

    # each email will be an array that has from, subject, and message
    all_emails = []
    for i in range(0, num_messages):
        raw_email = b"\n".join(pop_conn.retr(i+1)[1])
        parsed_email = email.message_from_bytes(raw_email)
        if "google" not in parsed_email["From"]:
            if parsed_email.is_multipart():
                parts = []
                for part in parsed_email.get_payload():
                    parts.append(part.get_payload())
                message = " ".join(parts)
            else:
                message = parsed_email.get_payload()
        all_emails.append([parsed_email["From"], parsed_email["Subject"], message])
    return json.dumps(all_emails)




if __name__ == "__main__":
    print(fetch_messages())

