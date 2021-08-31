"""
This module sends an email to tell a user that a specific host is online. It
does not actually check if the device is online in this module but instead
provides an email template that states that a device is online.
"""
from email.mime.text import MIMEText
from datetime import datetime
from getpass import getpass

import smtplib


class EmailUtility:
    # Set class attributes
    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 587
    DATE_FORMAT = '%#I:%M %p'
    EMAIL_SPACE = ', '

    def __init__(self):
        self.SMTP_USERNAME = None
        self.SMTP_PASSWORD = None
        self.mail = None

        while True:
            if self.smtp_login():
                break

        # Set the email to and from
        self.EMAIL_TO = [self.SMTP_USERNAME]
        self.EMAIL_FROM = self.SMTP_USERNAME

    def smtp_login(self):
        print('*** Make sure to turn on "Allow less secure apps" (https://myaccount.google.com/lesssecureapps) ***')

        # Get Gmail address
        email_address = input('Gmail username: ')
        self.SMTP_USERNAME = email_address

        # Get Gmail password without it showing in terminal
        password = getpass('Gmail password (no echo): ')
        self.SMTP_PASSWORD = password

        # Attempt to sign in
        try:
            self.mail = smtplib.SMTP(self.SMTP_SERVER, self.SMTP_PORT)
            self.mail.starttls()
            self.mail.login(self.SMTP_USERNAME, self.SMTP_PASSWORD)
            print('Gmail login successful.\n')
            return True
        except smtplib.SMTPAuthenticationError:
            print('There was an SMTP authentication error. Please try again. \n')
        return False

    def send_email(self, host):
        """Sends email stating that the host is now online"""
        try:
            msg = MIMEText('The host %s is now online.' % host)
            msg['To'] = self.EMAIL_SPACE.join(self.EMAIL_TO)
            msg['From'] = self.EMAIL_FROM
            msg['Subject'] = 'The host (' + host + ') is online - ' + (datetime.now().strftime(self.DATE_FORMAT))
            self.mail.sendmail(self.EMAIL_FROM, self.EMAIL_TO, msg.as_string())
            print('Email sent successfully.')
        except Exception as err:
            print(f'There was an error sending the email: {err}')

    def quit_smtp_session(self):
        self.mail.quit()


if __name__ == '__main__':
    """Send a test email if this module is called directly"""
    print('About to attempt a test email.\n')
    email = EmailUtility()
    email.send_email('test-device')
    email.quit_smtp_session()
    input('Email test complete. Press enter to exit. ')
