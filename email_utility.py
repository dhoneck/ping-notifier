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
    DATE_FORMAT = '%#I:%M %p'
    EMAIL_SPACE = ', '

    def __init__(self):
        self.SMTP_USERNAME = None
        self.SMTP_PASSWORD = None
        self.MAIL_SERVER = None
        self.SMTP_PORT = 587
        self.LOGIN_HELP_MESSAGE = None
        self.mail = None

        # Get mail SMTP settings
        print('What email would you like to use?')
        print('1. Gmail')
        print('2. Outlook/Hotmail/Live/MSN')
        print('3. Yahoo')
        while True:
            response = input('Enter the number here: ')
            print()

            if response == '1':
                self.SMTP_SERVER = 'smtp.gmail.com'
                self.MAIL_SERVER = 'Gmail'
                self.LOGIN_HELP_MESSAGE = '*** Make sure to turn on "Allow less secure apps" (' \
                                          'https://myaccount.google.com/lesssecureapps) *** '
                break
            elif response == '2':
                self.SMTP_SERVER = 'smtp-mail.outlook.com'
                self.MAIL_SERVER = 'Outlook/Hotmail/Live/MSN'
                break
            elif response == '3':
                self.SMTP_SERVER = 'smtp.mail.yahoo.com'
                self.MAIL_SERVER = 'Yahoo'
                self.SMTP_PORT = 465
                self.LOGIN_HELP_MESSAGE = '*** Make sure to generate an app password (' \
                                          'https://login.yahoo.com/myaccount/security/app-password) *** '
                break
            else:
                print('Not a valid option. Please try again.')

        # Attempt login
        while True:
            if self.smtp_login():
                break

        # Set the email to and from
        self.EMAIL_TO = [self.SMTP_USERNAME]
        self.EMAIL_FROM = self.SMTP_USERNAME

    def smtp_login(self):
        """Attempt to log into mail server with user provided credentials"""
        # Show login help message if there is one
        if self.LOGIN_HELP_MESSAGE:
            print(self.LOGIN_HELP_MESSAGE)

        # Get Gmail address
        email_address = input(f'{self.MAIL_SERVER} username: ')
        self.SMTP_USERNAME = email_address

        # Get Gmail password without it showing in terminal
        password = getpass(f'{self.MAIL_SERVER} password (no echo): ')
        self.SMTP_PASSWORD = password

        # Attempt to sign in
        try:
            if self.MAIL_SERVER == 'Yahoo':
                self.mail = smtplib.SMTP_SSL(self.SMTP_SERVER, self.SMTP_PORT)
                self.mail.ehlo()
            else:
                self.mail = smtplib.SMTP(self.SMTP_SERVER, self.SMTP_PORT)
                self.mail.starttls()

            self.mail.login(self.SMTP_USERNAME, self.SMTP_PASSWORD)
            print(f'{self.MAIL_SERVER} login successful.\n')
            return True
        except smtplib.SMTPAuthenticationError:
            print('There was an SMTP authentication error. Please try again. \n')
        except smtplib.SMTPConnectError:
            print('There was an SMTP connection error. Please try again. \n')
        except Exception as err:
            print(f'There was an error: {err}')
            print('Please try again. \n')
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
