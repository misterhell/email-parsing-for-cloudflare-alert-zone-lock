import imaplib
import os
import requests
from dotenv import load_dotenv

import logger
from logger import logger
from os import environ

load_dotenv()  # take environment variables from .env.

email = environ.get("EMAIL")
password = environ.get("PASSWORD")


class Notifier:
    @staticmethod
    def notify(message):
        print(f"Notification, {message}")


class CloudflareLocker:
    _api_key: str

    def __init__(self, api_key: str):
        self._api_key = api_key

    def lock_zone(self, zone_id):
        try:
            request_url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/settings/security_level"

            headers = {
                "Authorization": f"Bearer {self._api_key}",
                "Content-Type": "application/json"
            }

            data = {
                "value": "essentially_off"
            }

            response = requests.patch(request_url, headers=headers, json=data)

            if response.status_code == 200:
                pass
                # log success
                # send notification
            else:
                # log error
                # send notification
                print("Request failed with status code:", response.status_code)

        except Exception as e:
            logger.error(e)


def main():

    logger.info("Starting email checking")
    try:
        # Connect to the Gmail IMAP server
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        try:

            # Log in to your account
            mail.login(email, password)

            mailbox = "INBOX"
            mail.select(mailbox)

            # Search for unread emails
            status, data = mail.search(None, "UNSEEN")

            # Get the list of email IDs
            email_ids = data[0].split()

            # print(email_ids)

            # Search for unread emails
            # status, data = mail.search(None, "UNSEEN")

        except Exception as e:
            logger.error(e)
            Notifier.notify(f"Error on email parsing {e}")
            print(type(e), e)
        finally:
            mail.logout()

    except Exception as e:
        logger.error(f"Some high level error {e}")


if __name__ == '__main__':
    main()
