import requests
from logger import logger
from classes.cloudflare_alert import CloudflareAlert


class CloudflareLocker:
    _api_key: str

    def __init__(self, api_key: str):
        self._api_key = api_key

    def lock_zone(self, alert: CloudflareAlert):
        try:
            zone_id = ""
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
