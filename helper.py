def valid_email(email):
    return True if email.endswith('@cooper.edu') else False

def parse_emails(emails):
    return emails.split(', ')
