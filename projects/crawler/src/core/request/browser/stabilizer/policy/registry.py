from core.registry import Registry
from core.request.browser.stabilizer.policy.base import BrowserPageStabilityPolicy
from core.request.browser.typing import BrowserInteractionPhase

class BrowserPageStabilityPolicyRegistry(
    Registry[
        BrowserInteractionPhase,
        BrowserPageStabilityPolicy,
    ],
):
    """
    Registry of page stability policies.

    A policy is selected according to the current
    browser page runtime state.
    """

    def resolve(
        self,
        runtime_state: BrowserInteractionPhase,
    ) -> BrowserPageStabilityPolicy:
        policy = self.get_optional(runtime_state)

        if policy is not None:
            return policy

        raise RegistryKeyError(
            "No stability policy registered for "
            f"runtime state {runtime_state!r}.",
        )