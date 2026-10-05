from dataclasses import dataclass
from core.request.browser.snapshot import BrowserPageSnapshot
from core.request.browser.stabilizer.policy.base import BrowserPageStabilityPolicy


@dataclass(frozen=True, slots=True)
class StrictStabilityPolicy(
    BrowserPageStabilityPolicy,
):

    interval: float = 0.3
    max_attempts: int = 10

    def is_stable(
        self,
        previous: BrowserPageSnapshot,
        current: BrowserPageSnapshot,
    ) -> bool:

        return (
            previous.url
            == current.url
            and previous.title
            == current.title
            and previous.body_text
            == current.body_text
            and previous.status_code
            == current.status_code
            and previous.content_type
            == current.content_type
            and previous.has_body
            == current.has_body
            and previous.has_forms
            == current.has_forms
            and previous.has_inputs
            == current.has_inputs
            and previous.has_iframes
            == current.has_iframes
        )