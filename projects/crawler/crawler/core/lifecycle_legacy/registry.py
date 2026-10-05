
class LifecycleRegistry(
    MultiRegistry[
        LifecycleStage,
        type[LifecycleHook],
    ],
):
    pass