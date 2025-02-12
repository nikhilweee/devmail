import requests
import email
import json


class DevMail:

    def __init__(self):
        self.username = None
        self.token = None
        self.raw = None
        self.mailids = []
        self.parser = email.parser.Parser()

    def __repr__(self):
        return f'DevMail(username={self.username}, mailids={len(self.mailids)})'

    def parse_mail(self, mail_str):
        mail_object = self.parser.parsestr(mail_str)
        return dict(mail_object)

    def create(self):
        headers = {
            'accept': 'application/json',
        }

        if self.username:
            pass
        else:
            self.response = requests.put(
                'https://www.developermail.com/api/v1/mailbox', headers=headers)
            self.response = self.response.json()
            self.username = self.response['result']['name']
            self.token = self.response['result']['token']
        return {'username': self.username, 'token': self.token}

    def destroy(self):
        headers = {
            'accept': 'application/json',
            'X-MailboxToken': self.token,
        }
        self.response = requests.delete(
            f'https://www.developermail.com/api/v1/mailbox/{self.username}', headers=headers)
        self.response = self.response.json()
        self.username = None
        self.token = None
        return self.response

    def newtoken(self):
        headers = {
            'accept': 'application/json',
            'X-MailboxToken': self.token,
        }
        self.response = requests.put(
            f'https://www.developermail.com/api/v1/mailbox/{self.username}/token', headers=headers)
        self.response = self.response.json()
        self.token = self.response['result']['token']
        return {'username': self.username, 'token': self.token}

    def getmailids(self):
        headers = {
            'accept': 'application/json',
            'X-MailboxToken': self.token,
        }

        self.response = requests.get(
            f'https://www.developermail.com/api/v1/mailbox/{self.username}', headers=headers)
        self.response = self.response.json()
        self.mailids = self.response['result']
        return self.mailids

    def getmails(self, mailids: list=None, raw=False):
        headers = {
            'accept': 'application/json',
            'X-MailboxToken': self.token,
            'Content-Type': 'application/json',
        }

        if mailids is None:
            mailids = self.mailids

        data = json.dumps(mailids)

        self.response = requests.post(
            f'https://www.developermail.com/api/v1/mailbox/{self.username}/messages', headers=headers, data=data)
        self.response = self.response.json()
        mails = self.response['result']
        if not raw:
            for mail in mails:
                mail['value'] = self.parse_mail(mail['value'])
        return mails

    def getmail(self, mailid: str, raw=False):
        headers = {
            'accept': 'application/json',
            'X-MailboxToken': self.token,
        }
        self.response = requests.get(
            f'https://www.developermail.com/api/v1/mailbox/{self.username}/messages/{mailid}', headers=headers)
        self.response = self.response.json()
        mail = self.response['result']
        if not raw:
            mail = self.parse_mail(mail)
            # mail = email.message_from_string(mail)
        return mail

    def delmail(self, mailid: str):
        headers = {
            'accept': 'application/json',
            'X-MailboxToken': self.token,
        }
        self.response = requests.delete(
            f'https://www.developermail.com/api/v1/mailbox/{self.username}/messages/{mailid}', headers=headers)
        self.response = self.response.json()
        return self.response

    def sendmail(self, data: dict = None):
        headers = {
            'accept': 'application/json',
            'X-MailboxToken': self.token,
            'Content-Type': 'application/json',
        }

        data = json.dumps(data)

        self.response = requests.put(
            f'https://www.developermail.com/api/v1/mailbox/{self.username}/messages', headers=headers, data=data)
        self.response = self.response.json()
        return self.response
