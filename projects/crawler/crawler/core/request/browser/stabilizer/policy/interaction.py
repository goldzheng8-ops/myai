from dataclasses import dataclass
from core.request.browser.snapshot import BrowserPageSnapshot
from core.request.browser.stabilizer.policy.base import BrowserPageStabilityPolicy


@dataclass(frozen=True, slots=True)
class InteractionStabilityPolicy(
    BrowserPageStabilityPolicy,
):

    interval: float = 0.2
    max_attempts: int = 5

    def is_stable(
        self,
        previous: BrowserPageSnapshot,
        current: BrowserPageSnapshot,
    ) -> bool:

        if previous.url != current.url:
            return False

        if previous.title != current.title:
            return False

        return (
            previous.body_text
            == current.body_text
        )