import imaplib
import email
from email.message import Message
from classes.cloudflare_alert import CloudflareAlert
from typing import List
import re
from logger import logger


class CloudflareAlertsParser:

    _imap_conn: imaplib.IMAP4_SSL = None

    def __init__(self, imap_conn: imaplib.IMAP4_SSL):
        self._imap_conn = imap_conn

    def parse_inbox(self) -> List[CloudflareAlert]:
        mailbox = "INBOX"
        self._imap_conn.select(mailbox)

        # Search for unread emails
        status, data = self._imap_conn.search(None, "UNSEEN")

        # Get the list of email IDs
        email_ids = data[0].split()

        cloudflare_emails = []
        # Iterate over the email message IDs and parse each email
        for msg_id in email_ids:
            _, data = self._imap_conn.fetch(msg_id, '(RFC822)')
            raw_email = data[0][1]
            msg = email.message_from_bytes(raw_email)

            if "noreply@notify.cloudflare.com" in msg["From"] and "DDoS Attack Detected" in msg["Subject"]:
                alert_message = self._parse_cloudflare_emails(msg)
                if alert_message is not None:
                    cloudflare_emails.append(alert_message)

        return cloudflare_emails

    def _parse_cloudflare_emails(self, msg: Message):
        # Extracting email body
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                if content_type == 'text/plain':
                    body = part.get_payload(decode=True).decode('utf-8')
                    break
        else:
            body = msg.get_payload(decode=True).decode('utf-8')

        try:
            target_zone = re.search(r"Target zone: (.+)", body).group(1)
            target_hostname = re.search(r"Target hostname: (.+)", body).group(1)
            rule_id = re.search(r"Rule ID: (.+)", body).group(1)
            rule_override_id = ""
            rule_override_id_search = re.search(r"Rule override ID: (.+)", body)
            if rule_override_id_search:
                rule_override_id = rule_override_id_search.group(1)
            rule_link = re.search(r"View Rule: (.+)", body).group(1)

            return CloudflareAlert(
                target_zone.replace('\r', ''),
                target_hostname.replace('\r', ''),
                rule_id.replace('\r', ''),
                rule_override_id.replace('\r', ''),
                rule_link.replace('\r', '')
            )
        except Exception as e:
            logger.error("Parsing email data exception", exc_info=e)

        return None




