import imaplib
import time
import telebot
from dotenv import load_dotenv

import logger
from logger import logger
from os import environ

import schedule

from classes.email_parser import CloudflareAlertsParser
from classes.notifier import Notifier

load_dotenv()  # take environment variables from .env.

login = environ.get("EMAIL")
password = environ.get("PASSWORD")

bot_token = environ.get("TG_BOT_TOKEN")
chat_id = environ.get("TG_CHAT_ID")

def check_email_and_notify():
    logger.info("Starting email checking")
    try:
        # Connect to the Gmail IMAP server
        imap_conn = imaplib.IMAP4_SSL("imap.gmail.com")
        try:
            # Log in to your account
            imap_conn.login(login, password)

            parsed_alerts = CloudflareAlertsParser(imap_conn).parse_inbox()

            bot = telebot.TeleBot(bot_token)
            for alert in parsed_alerts:
                try:
                    bot.send_message(
                        chat_id,
                        f"Alert! DDos Attack \n"
                        f"Host: {alert.target_hostname} \n"
                        f"Zone: {alert.target_zone} \n"
                        f"Rule ID: {alert.rule_id} \n"
                        f"Rule link: <a href='{alert.rule_link}'>link</a>",
                        parse_mode="html"
                    )
                except Exception as e:
                    logger.error(e)

        except Exception as e:
            logger.error(e)
            Notifier.notify(f"Error on email parsing {e}")
        finally:
            imap_conn.close()

    except Exception as e:
        logger.error(f"Some high level error {e}")


schedule.every(1).minutes.do(check_email_and_notify)


def main():
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    main()
