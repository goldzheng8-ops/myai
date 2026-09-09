from dataclasses import dataclass
from urllib.robotparser import RobotFileParser


@dataclass(slots=True)
class RobotsCacheEntry:

    parser: RobotFileParser
    expires_at: float