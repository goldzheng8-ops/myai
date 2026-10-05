from dataclasses import dataclass
from core.request.browser.snapshot import BrowserPageSnapshot
from core.request.browser.stabilizer.policy.base import BrowserPageStabilityPolicy


@dataclass(frozen=True, slots=True)
class ChallengeStabilityPolicy(
    BrowserPageStabilityPolicy,
):

    interval: float = 0.5
    max_attempts: int = 10

    def is_stable(
        self,
        previous: BrowserPageSnapshot,
        current: BrowserPageSnapshot,
    ) -> bool:

        if previous.url != current.url:
            return False

        if previous.title != current.title:
            return False

        if (
            previous.has_iframes
            != current.has_iframes
        ):
            return False

        if (
            previous.has_forms
            != current.has_forms
        ):
            return False

        return (
            previous.body_text
            == current.body_text
        )