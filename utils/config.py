from dataclasses import dataclass, field
from typing import List
import yaml


@dataclass
class Config:
    url: str
    badge_numbers: List[str]
    user_mention: str
    webhook_url: str

    @classmethod
    def from_yaml(cls, path: str) -> "Config":
        with open(path, "r") as f:
            data = yaml.safe_load(f)
        return cls(
            url=data["url"],
            badge_numbers=[str(b) for b in data["badge_numbers"]],
            user_mention=data["user_mention"],
            webhook_url=data["webhook_url"],
        )

    @classmethod
    def from_string(cls, yaml_string: str) -> "Config":
        data = yaml.safe_load(yaml_string)
        return cls(
            url=data["url"],
            badge_numbers=[str(b) for b in data["badge_numbers"]],
            user_mention=data["user_mention"],
            webhook_url=data["webhook_url"],
        )