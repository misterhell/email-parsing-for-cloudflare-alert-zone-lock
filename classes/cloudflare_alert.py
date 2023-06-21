from dataclasses import dataclass


@dataclass
class CloudflareAlert:
    target_zone: str
    target_hostname: str
    rule_id: str
    rule_override_id: str
    rule_link: str
